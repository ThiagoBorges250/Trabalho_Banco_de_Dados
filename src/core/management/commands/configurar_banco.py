from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Cria o banco acadêmico no PostgreSQL, suas rotinas e dados iniciais."

    def handle(self, *args, **options):
        with transaction.atomic():
            with connection.cursor() as cursor:
                self.stdout.write("Criando tabelas...")

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alunos (
                        id_aluno SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        telefone VARCHAR(9),
                        cpf VARCHAR(11) UNIQUE NOT NULL,
                        email VARCHAR(100),
                        data_nascimento DATE NOT NULL
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS professores (
                        id_professor SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        cpf VARCHAR(11) UNIQUE NOT NULL,
                        email VARCHAR(100),
                        telefone VARCHAR(9),
                        data_nascimento DATE NOT NULL,
                        especialidade VARCHAR(100)
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS disciplinas (
                        id_disciplina SERIAL PRIMARY KEY,
                        nome_disciplina VARCHAR(100) NOT NULL,
                        carga_horaria INT NOT NULL,
                        fk_id_professor INT NOT NULL
                            REFERENCES professores(id_professor)
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS matricula (
                        id_matricula SERIAL PRIMARY KEY,
                        fk_id_aluno INT NOT NULL
                            REFERENCES alunos(id_aluno),
                        fk_id_disciplina INT NOT NULL
                            REFERENCES disciplinas(id_disciplina),
                        data_matricula DATE NOT NULL,
                        nota1 DOUBLE PRECISION CHECK (nota1 >= 0 AND nota1 <= 10),
                        nota2 DOUBLE PRECISION CHECK (nota2 >= 0 AND nota2 <= 10),
                        nota3 DOUBLE PRECISION CHECK (nota3 >= 0 AND nota3 <= 10),
                        status VARCHAR(50) CHECK (
                            status IN ('aprovado', 'reprovado', 'matriculado', 'cancelado')
                        ),
                        UNIQUE (fk_id_aluno, fk_id_disciplina)
                    )
                """)

                # Garante que instalações antigas também tenham a estrutura atual.
                cursor.execute("""
                    ALTER TABLE matricula
                    ADD COLUMN IF NOT EXISTS nota1 DOUBLE PRECISION
                """)
                cursor.execute("""
                    ALTER TABLE matricula
                    ADD COLUMN IF NOT EXISTS nota2 DOUBLE PRECISION
                """)
                cursor.execute("""
                    ALTER TABLE matricula
                    ADD COLUMN IF NOT EXISTS nota3 DOUBLE PRECISION
                """)

                cursor.execute("""
                    ALTER TABLE matricula
                    DROP CONSTRAINT IF EXISTS matricula_status_check
                """)
                cursor.execute("""
                    ALTER TABLE matricula
                    ADD CONSTRAINT matricula_status_check
                    CHECK (status IN ('aprovado', 'reprovado', 'matriculado', 'cancelado'))
                """)

                self.stdout.write("Criando View, Function e Procedures...")

                cursor.execute("""
                    CREATE OR REPLACE VIEW vw_relatorio_alunos AS
                    SELECT
                        a.id_aluno,
                        a.nome AS aluno,
                        d.id_disciplina,
                        d.nome_disciplina AS disciplina,
                        p.nome AS professor,
                        m.nota1,
                        m.nota2,
                        m.nota3,
                        m.status,
                        m.data_matricula
                    FROM matricula m
                    INNER JOIN alunos a
                        ON m.fk_id_aluno = a.id_aluno
                    INNER JOIN disciplinas d
                        ON m.fk_id_disciplina = d.id_disciplina
                    INNER JOIN professores p
                        ON d.fk_id_professor = p.id_professor
                    WHERE m.nota1 IS NOT NULL
                       OR m.nota2 IS NOT NULL
                       OR m.nota3 IS NOT NULL
                """)

                cursor.execute("""
                    CREATE OR REPLACE FUNCTION calcular_media_aluno(p_id_aluno INTEGER)
                    RETURNS NUMERIC(4,2)
                    LANGUAGE plpgsql
                    AS $$
                    DECLARE
                        v_media NUMERIC(4,2);
                    BEGIN
                        SELECT AVG((nota1 + nota2 + nota3) / 3)
                        INTO v_media
                        FROM matricula
                        WHERE fk_id_aluno = p_id_aluno
                          AND nota1 IS NOT NULL
                          AND nota2 IS NOT NULL
                          AND nota3 IS NOT NULL;

                        RETURN COALESCE(v_media, 0);
                    END;
                    $$;
                """)

                cursor.execute("""
                    CREATE OR REPLACE PROCEDURE realizar_matricula(
                        p_id_aluno INTEGER,
                        p_id_disciplina INTEGER
                    )
                    LANGUAGE plpgsql
                    AS $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM alunos WHERE id_aluno = p_id_aluno
                        ) THEN
                            RAISE EXCEPTION 'Aluno não encontrado.';
                        END IF;

                        IF NOT EXISTS (
                            SELECT 1 FROM disciplinas
                            WHERE id_disciplina = p_id_disciplina
                        ) THEN
                            RAISE EXCEPTION 'Disciplina não encontrada.';
                        END IF;

                        IF EXISTS (
                            SELECT 1 FROM matricula
                            WHERE fk_id_aluno = p_id_aluno
                              AND fk_id_disciplina = p_id_disciplina
                        ) THEN
                            RAISE EXCEPTION
                                'Aluno já está matriculado nesta disciplina.';
                        END IF;

                        INSERT INTO matricula (
                            fk_id_aluno,
                            fk_id_disciplina,
                            data_matricula,
                            nota1,
                            nota2,
                            nota3,
                            status
                        )
                        VALUES (
                            p_id_aluno,
                            p_id_disciplina,
                            CURRENT_DATE,
                            NULL,
                            NULL,
                            NULL,
                            'matriculado'
                        );

                        RAISE NOTICE 'Matrícula realizada com sucesso.';
                    END;
                    $$;
                """)

                cursor.execute("""
                    CREATE OR REPLACE PROCEDURE cancelar_matricula(
                        p_id_aluno INTEGER,
                        p_id_disciplina INTEGER
                    )
                    LANGUAGE plpgsql
                    AS $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM matricula
                            WHERE fk_id_aluno = p_id_aluno
                              AND fk_id_disciplina = p_id_disciplina
                        ) THEN
                            RAISE EXCEPTION 'Matrícula não encontrada.';
                        END IF;

                        IF NOT EXISTS (
                            SELECT 1
                            FROM matricula
                            WHERE fk_id_aluno = p_id_aluno
                              AND fk_id_disciplina = p_id_disciplina
                              AND status = 'matriculado'
                        ) THEN
                            RAISE EXCEPTION
                                'A matrícula não está com status matriculado.';
                        END IF;

                        UPDATE matricula
                        SET status = 'cancelado'
                        WHERE fk_id_aluno = p_id_aluno
                          AND fk_id_disciplina = p_id_disciplina;

                        RAISE NOTICE 'Matrícula cancelada com sucesso.';
                    END;
                    $$;
                """)

                self.stdout.write("Inserindo dados iniciais...")

                alunos = [
                    ('Ana Beatriz Silva', '999999999', '12345678901', 'ana@email.com', '2004-05-10'),
                    ('Carlos Henrique Souza', '988888888', '23456789012', 'carlos@email.com', '2003-08-22'),
                    ('Mariana Oliveira Lima', '977777777', '34567890123', 'mariana@email.com', '2005-01-15'),
                    ('João Vitor Pereira', '966666666', '45612378901', 'joao@email.com', '2002-11-20'),
                ]
                for aluno in alunos:
                    cursor.execute("""
                        INSERT INTO alunos (nome, telefone, cpf, email, data_nascimento)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (cpf) DO NOTHING
                    """, aluno)

                professores = [
                    ('João Pedro Almeida', '45678901234', 'joao.prof@email.com', '966666666', '1980-03-12', 'Banco de Dados'),
                    ('Fernanda Costa Ribeiro', '56789012345', 'fernanda@email.com', '955555555', '1985-07-19', 'Programação'),
                    ('Ricardo Mendes Santos', '67890123456', 'ricardo@email.com', '944444444', '1979-11-25', 'Engenharia de Software'),
                ]
                for professor in professores:
                    cursor.execute("""
                        INSERT INTO professores (
                            nome, cpf, email, telefone, data_nascimento, especialidade
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (cpf) DO NOTHING
                    """, professor)

                disciplinas = [
                    ('Banco de Dados I', 60, '45678901234'),
                    ('Algoritmos', 80, '56789012345'),
                    ('Engenharia de Software', 60, '67890123456'),
                ]
                for nome, carga, cpf_professor in disciplinas:
                    cursor.execute("""
                        INSERT INTO disciplinas (
                            nome_disciplina, carga_horaria, fk_id_professor
                        )
                        SELECT %s, %s, id_professor
                        FROM professores
                        WHERE cpf = %s
                          AND NOT EXISTS (
                              SELECT 1
                              FROM disciplinas
                              WHERE nome_disciplina = %s
                          )
                    """, (nome, carga, cpf_professor, nome))

                matriculas = [
                    ('12345678901', 'Banco de Dados I', '2026-10-01', 8.5, 7.5, 9.0, 'aprovado'),
                    ('12345678901', 'Algoritmos', '2026-10-01', 7.0, 8.0, 6.5, 'aprovado'),
                    ('23456789012', 'Banco de Dados I', '2026-10-01', 6.0, 5.5, 7.0, 'reprovado'),
                    ('23456789012', 'Engenharia de Software', '2026-10-01', 9.0, 8.5, 10.0, 'aprovado'),
                    ('34567890123', 'Algoritmos', '2026-10-01', 5.0, 6.0, 4.5, 'reprovado'),
                    ('34567890123', 'Engenharia de Software', '2026-10-01', 7.0, 8.0, 7.5, 'matriculado'),
                    ('45612378901', 'Algoritmos', '2026-10-01', 8.5, 9.0, 8.0, 'aprovado'),
                ]
                for cpf_aluno, nome_disciplina, data, n1, n2, n3, status in matriculas:
                    cursor.execute("""
                        INSERT INTO matricula (
                            fk_id_aluno,
                            fk_id_disciplina,
                            data_matricula,
                            nota1,
                            nota2,
                            nota3,
                            status
                        )
                        SELECT a.id_aluno, d.id_disciplina, %s, %s, %s, %s, %s
                        FROM alunos a
                        CROSS JOIN disciplinas d
                        WHERE a.cpf = %s
                          AND d.nome_disciplina = %s
                          AND NOT EXISTS (
                              SELECT 1
                              FROM matricula m
                              WHERE m.fk_id_aluno = a.id_aluno
                                AND m.fk_id_disciplina = d.id_disciplina
                          )
                    """, (data, n1, n2, n3, status, cpf_aluno, nome_disciplina))

                # Corrige o status da matrícula sem notas, quando houver uma já criada.
                cursor.execute("""
                    UPDATE matricula
                    SET status = CASE
                        WHEN status = 'cancelado' THEN 'cancelado'
                        WHEN nota1 IS NULL AND nota2 IS NULL AND nota3 IS NULL
                            THEN 'matriculado'
                        WHEN nota1 IS NOT NULL AND nota2 IS NOT NULL AND nota3 IS NOT NULL
                            THEN CASE
                                WHEN (nota1 + nota2 + nota3) / 3 >= 7
                                    THEN 'aprovado'
                                ELSE 'reprovado'
                            END
                        ELSE status
                    END
                """)

                # Mantém as sequências acima do maior ID inserido, inclusive em
                # instalações que receberam dados com IDs explícitos anteriormente.
                for tabela, coluna, sequencia in [
                    ('alunos', 'id_aluno', 'alunos_id_aluno_seq'),
                    ('professores', 'id_professor', 'professores_id_professor_seq'),
                    ('disciplinas', 'id_disciplina', 'disciplinas_id_disciplina_seq'),
                    ('matricula', 'id_matricula', 'matricula_id_matricula_seq'),
                ]:
                    cursor.execute(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{tabela}', '{coluna}'),
                            COALESCE((SELECT MAX({coluna}) FROM {tabela}), 1),
                            EXISTS (SELECT 1 FROM {tabela})
                        )
                    """)

        self.stdout.write(self.style.SUCCESS(
            "Banco configurado com sucesso: tabelas, View, Function, Procedures e dados iniciais."
        ))
