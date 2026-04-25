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
    fk_id_aluno INT NOT NULL REFERENCES alunos(id_aluno),
    fk_id_disciplina INT NOT NULL REFERENCES disciplinas(id_disciplina),
    data_matricula DATE NOT NULL,
    nota REAL CHECK (nota >= 0 AND nota <= 10),
    status VARCHAR(50) CHECK (status IN ('aprovado', 'reprovado', 'matriculado')),
    UNIQUE (fk_id_aluno, fk_id_disciplina)
);