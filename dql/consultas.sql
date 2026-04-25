SELECT * FROM alunos;

SELECT * FROM professores;

SELECT * FROM disciplinas;

SELECT * FROM matricula;

SELECT nome, id_aluno FROM alunos
ORDER BY nome ASC;

SELECT nome, id_aluno FROM alunos
ORDER BY nome DESC;

SELECT nome, data_nascimento FROM alunos
ORDER BY data_nascimento DESC;

SELECT nome, data_nascimento FROM alunos
ORDER BY data_nascimento ASC;

SELECT nome, nome_disciplina, nota FROM matricula
INNER JOIN alunos ON fk_id_aluno = id_aluno
INNER JOIN disciplinas ON fk_id_disciplina = id_disciplina;

SELECT nome, nome_disciplina FROM alunos
LEFT JOIN matricula ON id_aluno = fk_id_aluno
LEFT JOIN disciplinas ON fk_id_disciplina = id_disciplina;

SELECT a.nome, d.nome_disciplina, p.nome AS professor, nota FROM matricula
INNER JOIN alunos a ON fk_id_aluno = id_aluno
INNER JOIN disciplinas d ON fk_id_disciplina = id_disciplina
INNER JOIN professores p ON fk_id_professor = id_professor;

SELECT a.nome, d.nome_disciplina, m.nota
FROM matricula m
INNER JOIN alunos a ON m.fk_id_aluno = a.id_aluno
INNER JOIN disciplinas d ON m.fk_id_disciplina = d.id_disciplina
WHERE m.status = 'aprovado';

SELECT a.nome, d.nome_disciplina, m.nota
FROM matricula m
INNER JOIN alunos a ON m.fk_id_aluno = a.id_aluno
INNER JOIN disciplinas d ON m.fk_id_disciplina = d.id_disciplina
WHERE m.status = 'reprovado';

SELECT a.nome AS aluno, d.nome_disciplina
FROM alunos a
FULL OUTER JOIN matricula m ON a.id_aluno = m.fk_id_aluno
FULL OUTER JOIN disciplinas d ON m.fk_id_disciplina = d.id_disciplina;