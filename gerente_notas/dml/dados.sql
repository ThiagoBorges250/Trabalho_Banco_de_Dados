INSERT INTO alunos (nome, telefone, cpf, email, data_nascimento) VALUES
('Ana Beatriz Silva', '999999999', '12345678901', 'ana@email.com', '2004-05-10'),
('Carlos Henrique Souza', '988888888', '23456789012', 'carlos@email.com', '2003-08-22'),
('Mariana Oliveira Lima', '977777777', '34567890123', 'mariana@email.com', '2005-01-15');

INSERT INTO professores (nome, cpf, email, telefone, data_nascimento, especialidade) VALUES
('João Pedro Almeida', '45678901234', 'joao@email.com', '966666666', '1980-03-12', 'Banco de Dados'),
('Fernanda Costa Ribeiro', '56789012345', 'fernanda@email.com', '955555555', '1985-07-19', 'Programação'),
('Ricardo Mendes Santos', '67890123456', 'ricardo@email.com', '944444444', '1979-11-25', 'Engenharia de Software');

INSERT INTO disciplinas (nome_disciplina, carga_horaria, fk_id_professor) VALUES
('Banco de Dados I', 60, 1),
('Algoritmos', 80, 2),
('Engenharia de Software', 60, 3);

INSERT INTO matricula (fk_id_aluno, fk_id_disciplina, data_matricula, nota, status) VALUES
(1, 1, '2026-04-10', 8.5, 'aprovado'),
(1, 2, '2026-04-10', 7.0, 'aprovado'),
(2, 1, '2026-04-11', 6.0, 'reprovado'),
(2, 3, '2026-04-11', 9.0, 'aprovado'),
(3, 2, '2026-04-12', 5.5, 'reprovado'),
(3, 3, '2026-04-12', 0.0, 'matriculado');

UPDATE matricula SET nota = 5.0 
WHERE fk_id_aluno = 3 AND fk_id_disciplina = 2;

UPDATE matricula SET nota = 8.0 
WHERE fk_id_aluno = 3 AND fk_id_disciplina = 3;

UPDATE matricula SET status = 'aprovado'
WHERE fk_id_aluno = 3 AND fk_id_disciplina = 3;

DELETE FROM matricula 
WHERE fk_id_disciplina = 3;

DELETE FROM disciplinas
WHERE nome_disciplina = 'Engenharia de Software';

INSERT INTO alunos (nome, telefone, cpf, email, data_nascimento) VALUES
('João Vitor Pereira', '966666666', '45612378901', 'joao@email.com', '2002-11-20'),
('Camila Fernandes Rocha', '955555555', '56723489012', 'camila@email.com', '2003-06-14'),
('Lucas Gabriel Martins', '944444444', '67834590123', 'lucas@email.com', '2001-09-30'),
('Beatriz Alves Souza', '933333333', '78945601234', 'beatriz@email.com', '2004-12-05'),
('Rafael Henrique Gomes', '922222222', '89056712345', 'rafael@email.com', '2002-03-18'),
('Juliana Costa Mendes', '911111111', '90167823456', 'juliana@email.com', '2005-07-22');