-- Criar o banco antes:  CREATE DATABASE "Gerente_Notas";
-- As tabelas são mapeadas pelo Django com managed = False, então este script
-- precisa ser executado no banco ANTES de rodar o sistema.

CREATE TABLE alunos(
    nome VARCHAR(100) NOT NULL,
    id_aluno SERIAL PRIMARY KEY,
    telefone VARCHAR(9),
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    data_nascimento DATE NOT NULL
);

CREATE TABLE professores(
    nome VARCHAR(100) NOT NULL,
    id_professor SERIAL PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(9),
    data_nascimento DATE NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE disciplinas(
    id_disciplina SERIAL PRIMARY KEY,
    nome_disciplina VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL,
    fk_id_professor INT NOT NULL REFERENCES professores(id_professor)
);

CREATE TABLE matricula(
    id_matricula SERIAL PRIMARY KEY,
    fk_id_aluno INT NOT NULL REFERENCES alunos(id_aluno) ON DELETE CASCADE,
    fk_id_disciplina INT NOT NULL REFERENCES disciplinas(id_disciplina) ON DELETE CASCADE,
    data_matricula DATE NOT NULL DEFAULT CURRENT_DATE,
    nota1 REAL CHECK (nota1 >= 0 AND nota1 <= 10),
    nota2 REAL CHECK (nota2 >= 0 AND nota2 <= 10),
    nota3 REAL CHECK (nota3 >= 0 AND nota3 <= 10),
    status VARCHAR(50) CHECK (status IN ('aprovado', 'reprovado', 'matriculado', 'cancelado')),
    UNIQUE (fk_id_aluno, fk_id_disciplina)
);

-- ─── VIEW usada em /relatorio-view/ ─────────────────────────────────────────
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
INNER JOIN alunos a ON m.fk_id_aluno = a.id_aluno
INNER JOIN disciplinas d ON m.fk_id_disciplina = d.id_disciplina
INNER JOIN professores p ON d.fk_id_professor = p.id_professor;

-- ─── FUNCTION usada em /media-aluno/ ────────────────────────────────────────
-- Média geral das disciplinas com as 3 notas lançadas (NULL se não houver).
CREATE OR REPLACE FUNCTION calcular_media_aluno(p_id_aluno INT)
RETURNS NUMERIC AS $$
    SELECT ROUND(AVG((nota1 + nota2 + nota3) / 3.0)::numeric, 2)
    FROM matricula
    WHERE fk_id_aluno = p_id_aluno
      AND nota1 IS NOT NULL AND nota2 IS NOT NULL AND nota3 IS NOT NULL;
$$ LANGUAGE SQL STABLE;

-- ─── PROCEDURE usada ao matricular (CALL realizar_matricula) ────────────────
CREATE OR REPLACE PROCEDURE realizar_matricula(p_id_aluno INT, p_id_disciplina INT)
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM alunos WHERE id_aluno = p_id_aluno) THEN
        RAISE EXCEPTION 'Aluno não encontrado.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM disciplinas WHERE id_disciplina = p_id_disciplina) THEN
        RAISE EXCEPTION 'Disciplina não encontrada.';
    END IF;
    IF EXISTS (SELECT 1 FROM matricula
               WHERE fk_id_aluno = p_id_aluno AND fk_id_disciplina = p_id_disciplina) THEN
        RAISE EXCEPTION 'Aluno já matriculado nesta disciplina.';
    END IF;

    INSERT INTO matricula (fk_id_aluno, fk_id_disciplina, data_matricula, status)
    VALUES (p_id_aluno, p_id_disciplina, CURRENT_DATE, 'matriculado');
END;
$$;
