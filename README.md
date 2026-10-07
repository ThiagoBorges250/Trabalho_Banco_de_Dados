# 📚 Sistema Gerente de Notas

## 🪪 Identificação

| | |
|---|---|
| **Integrante** | Thiago Borges (trabalho individual) |
| **Disciplina** | Banco de Dados |
| **Professor** | Anderson Costa |
| **Instituição** | UniFSA – Centro Universitário Santo Agostinho |
| **Trabalho** | Trabalho Avaliativo – Projeto de Banco de Dados (evolução do CRUD anterior – Opção 1) |

---

## 📌 Sobre o projeto

O **Gerente de Notas** é um sistema acadêmico web para controlar **alunos, professores, disciplinas, matrículas e notas**.
Ele resolve o problema de manter o histórico de notas espalhado: o professor lança as 3 notas de cada aluno por disciplina e o sistema calcula a média, define a situação (**Aprovado / Reprovado / Matriculado**, média mínima **7,0**) e gera relatórios consolidados.

Funcionalidades principais:

* 🔐 Login
* CRUD completo de alunos, professores e disciplinas (com busca e ordenação)
* Matrícula de alunos em disciplinas
* Lançamento de 3 notas por matrícula, com média e status automáticos
* Dashboard com totais e relatórios (INNER JOIN, LEFT JOIN, FULL OUTER JOIN)
* Relatório de notas por disciplina, consulta de média e boletim do aluno

---

## 🛠 Tecnologias utilizadas

```
Python 3
Django 4.2
PostgreSQL
HTML / CSS / Bootstrap 5
Git e GitHub
```

---

## 🗄️ Banco de dados

**SGBD:** PostgreSQL

**Principais tabelas**

| Tabela | Descrição |
|---|---|
| `alunos` | dados dos alunos (PK `id_aluno`, CPF único) |
| `professores` | dados dos professores e especialidade |
| `disciplinas` | disciplinas, carga horária e professor responsável (FK → `professores`) |
| `matricula` | liga aluno e disciplina (FKs), com `nota1`, `nota2`, `nota3` e `status` |

Relacionamentos: um professor ministra várias disciplinas; um aluno se matricula em várias disciplinas; `matricula` conecta alunos e disciplinas (único por par aluno/disciplina).

### Recursos avançados (View, Function e Procedure)

| Recurso | Script | Finalidade | Onde é usado no sistema |
|---|---|---|---|
| **View** `vw_relatorio_alunos` | `database/views/vw_relatorio_alunos.sql` | Junta (4 INNER JOIN) matrícula, aluno, disciplina e professor, entregando notas e status prontos para relatório | Tela **Relatório (View)** – `/relatorio-view/`, com filtro por disciplina |
| **Function** `calcular_media_aluno(id)` | `database/functions/calcular_media_aluno.sql` | Recebe o id do aluno e retorna a média geral das disciplinas que já têm as 3 notas (`NULL` se não houver) | Tela **Média do aluno** – `/media-aluno/` (média geral e boletim) |
| **Procedure** `realizar_matricula(aluno, disciplina)` | `database/procedures/realizar_matricula.sql` | Valida aluno e disciplina, impede matrícula duplicada (`RAISE EXCEPTION`) e insere a matrícula com status `matriculado` | Tela **Matricular aluno** – `/matriculas/novo/` (`CALL realizar_matricula(...)`) |

Fluxo integrado: **tela do sistema → chamada ao banco → View/Function/Procedure → resultado exibido na aplicação.**
O código das chamadas está em `src/core/views.py` (`relatorio_view`, `media_aluno`, `matricula_create`).

---

## 🗂 Estrutura do repositório

```
gerente_notas/
├── src/                      # código-fonte da aplicação Django
├── database/
│   ├── tables/               # criação das tabelas
│   ├── views/                # View
│   ├── functions/            # Function
│   ├── procedures/           # Procedure
│   └── inserts/              # dados de teste
├── docs/                     # consultas JOIN e exemplos de UPDATE/DELETE
├── requirements.txt
└── README.md
```

---

## ▶️ Como executar

Pré-requisitos: Python 3.10+ e PostgreSQL instalados.

```bash
# 1. Criar o banco
createdb Gerente_Notas

# 2. Criar tabelas, view, function, procedure e dados de teste (nesta ordem)
psql -d Gerente_Notas -f database/tables/01_tabelas.sql
psql -d Gerente_Notas -f database/views/vw_relatorio_alunos.sql
psql -d Gerente_Notas -f database/functions/calcular_media_aluno.sql
psql -d Gerente_Notas -f database/procedures/realizar_matricula.sql
psql -d Gerente_Notas -f database/inserts/dados.sql

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Preparar o Django e criar o usuário de login
cd src
python manage.py migrate
python manage.py createsuperuser

# 5. Rodar
python manage.py runserver
```

Acesse http://127.0.0.1:8000 e entre com o usuário criado.

> As tabelas são mapeadas pelo Django com `managed = False`, por isso os scripts SQL do passo 2 devem ser executados antes de usar o sistema.

**Conexão com o banco:** por padrão `postgresql://postgres:root@localhost:5432/Gerente_Notas`. Para usar outra, defina a variável de ambiente `DATABASE_URL` (ex.: `postgresql://usuario:senha@localhost:5432/Gerente_Notas`).

---

## 🌐 Acesso online e vídeo

* **Sistema (Render):** https://trabalho-banco-de-dados-wjy2.onrender.com/login/?next=/
  Usuário de teste: `Thiago` / senha `1234`. O plano gratuito pode demorar a carregar no primeiro acesso; use em computador.
* **Vídeo explicativo 1 (Joins):** https://drive.google.com/uc?id=1eb8qdmASeKHIpgChyErokfuOVIvIduei&export=download
* **Vídeo explicativo 2 (View, Function e Procedure):**

---

## ✅ Requisitos do trabalho atendidos

* ✔ 1 View, 1 Function e 1 Procedure, com finalidades diferentes, criadas no banco e usadas pela aplicação
* ✔ 3 telas/funcionalidades usando os recursos (Relatório View, Média do aluno, Matricular aluno)
* ✔ Scripts de tabelas, inserts, View, Function e Procedure organizados em `database/`
* ✔ Repositório no GitHub, README e vídeo explicativo