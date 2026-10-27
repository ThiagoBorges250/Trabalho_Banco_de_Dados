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
PostgreSQL (hospedado no Supabase)
Redis (cache e sessões)
HTML / CSS / Bootstrap 5
Git e GitHub
```

---

## 🗄️ Banco de dados

**SGBD:** PostgreSQL, hospedado no **Supabase** (em desenvolvimento local também funciona com um PostgreSQL próprio)

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
| **View** `vw_relatorio_alunos` | `ddl/schema.sql` e `configurar_banco` | Junta (4 INNER JOIN) matrícula, aluno, disciplina e professor, entregando notas e status prontos para relatório | Tela **Relatório (View)** – `/relatorio-view/`, com filtro por disciplina |
| **Function** `calcular_media_aluno(id)` | `ddl/schema.sql` e `configurar_banco` | Recebe o id do aluno e retorna a média geral das disciplinas que já têm as 3 notas (`NULL` se não houver) | Tela **Média do aluno** – `/media-aluno/` (média geral e boletim) |
| **Procedure** `realizar_matricula(aluno, disciplina)` | `ddl/schema.sql` e `configurar_banco` | Valida aluno e disciplina, impede matrícula duplicada (`RAISE EXCEPTION`) e insere a matrícula com status `matriculado` | Tela **Matricular aluno** – `/matriculas/novo/` (`CALL realizar_matricula(...)`) |

Fluxo integrado: **tela do sistema → chamada ao banco → View/Function/Procedure → resultado exibido na aplicação.**
O código das chamadas está em `src/core/views.py` (`relatorio_view`, `media_aluno`, `matricula_create`).

---

## 🗂 Estrutura do repositório

```
Trabalho_Banco_de_Dados/
├── src/                          # código-fonte da aplicação Django
│   ├── core/
│   │   ├── management/commands/
│   │   │   ├── configurar_banco.py   # cria tabelas, View, Function, Procedures e dados iniciais
│   │   │   └── criar_usuario.py      # cria o usuário de login
│   │   ├── cache_utils.py            # cache com Redis (HIT/MISS, invalidação)
│   │   └── supabase_client.py        # cliente da API do Supabase (opcional)
│   ├── gerente_notas/settings.py     # configuração (Supabase, Redis)
│   ├── teste_conexoes.py             # testa Supabase e Redis
│   ├── .env.example                  # modelo das variáveis de ambiente
│   └── manage.py
├── ddl/                          # criação das tabelas (schema.sql)
├── dml/                          # dados de teste
├── dql/                          # consultas (JOINs, filtros, ordenação)
├── requirements.txt
└── README.md
```

---

## 🔌 Integração com Supabase e Redis

| Serviço | Para que serve | Variável de ambiente |
|---|---|---|
| **Supabase** (PostgreSQL) | Banco de dados principal: tabelas, View, Function e Procedures | `DATABASE_URL` |
| **Supabase API** (opcional) | Acesso à API do Supabase por `core/supabase_client.py` | `SUPABASE_URL`, `SUPABASE_KEY` |
| **Redis** | **Cache de consultas** (Dashboard, Relatório da View, Média do aluno) e **sessões de login** | `REDIS_URL` |

Se `REDIS_URL` estiver vazia, o sistema usa cache em memória e continua funcionando. Se `DATABASE_URL` estiver vazia, usa o PostgreSQL local (`postgresql://postgres:root@localhost:5432/Gerente_Notas`).

### Como o Supabase é usado

O Supabase hospeda o **PostgreSQL** do sistema. Todas as tabelas (`alunos`, `professores`, `disciplinas`, `matricula`), a **View** `vw_relatorio_alunos`, a **Function** `calcular_media_aluno` e as **Procedures** `realizar_matricula` e `cancelar_matricula` ficam nele. A aplicação Django conecta pela `DATABASE_URL` (SSL obrigatório) e usa os dados em todas as telas: cadastros (CRUD), matrículas, lançamento de notas, relatórios, boletim e média do aluno. O Supabase é a fonte da verdade: o Redis nunca guarda nada que não esteja nele.

### Como o Redis é usado (e por que)

**Problema:** o banco fica na internet (Supabase). Telas como o **Dashboard** (7 consultas `COUNT`), o **Relatório (View)** (4 `JOIN`s) e a **Média do aluno** (Function + boletim) repetem as mesmas consultas a cada acesso, e cada ida ao banco custa tempo e consome conexões.

**Solução:** o Redis foi usado de duas formas:

| Uso | Onde no código | O que faz |
|---|---|---|
| **Cache de consultas** | `src/core/cache_utils.py`, usado em `dashboard`, `relatorio_view` e `media_aluno` (`src/core/views.py`) | A 1ª leitura vai ao Supabase e o resultado é guardado no Redis por 5 minutos; as seguintes saem do Redis (**cache HIT**) |
| **Sessões de login** | `SESSION_ENGINE` em `settings.py` | O login fica no Redis em vez da tabela de sessões do banco, evitando uma consulta ao banco por requisição |

**Invalidação (dados sempre corretos):** toda gravação (cadastrar, editar ou excluir aluno, professor, disciplina ou matrícula, lançar notas, ou chamar a procedure `realizar_matricula`) incrementa uma **versão dos dados** no Redis (`dados_versao`). As chaves de cache incluem essa versão (`dados:dashboard:v3`), então depois de qualquer alteração a próxima leitura vai ao Supabase e a tela nunca mostra dado desatualizado.

**Tolerância a falhas:** se o Redis ficar fora do ar, o sistema continua funcionando e consulta o Supabase direto.

**Benefícios:** respostas mais rápidas nas telas pesadas, menos consultas ao Supabase e sessões rápidas e centralizadas.

**Como ver funcionando (demonstração):**
1. Abra o **Dashboard**, o **Relatório (View)** ou a **Média do aluno**. Um selo no topo mostra a origem: 🟡 *Supabase (cache MISS)* na 1ª vez e 🟢 *Redis (cache HIT)* nas seguintes, com o tempo em ms.
2. Cadastre um aluno ou uma matrícula e volte ao Dashboard: o selo volta a *MISS* (cache invalidado) e o número já está atualizado.
3. Abra **Painel Redis** (menu *Infraestrutura*): ele mostra a conexão, acertos e erros de cache, a taxa de acerto, as chaves guardadas com o tempo de expiração (cache e sessões), o botão **Comparar tempos** (Supabase × Redis) e o botão **Limpar cache**.

### Capturas de tela

Adicione as imagens em `docs/img/` e referencie aqui:

```markdown
![Dashboard com cache do Redis](docs/img/dashboard-redis.png)
![Painel Redis](docs/img/painel-redis.png)
![Tabelas no Supabase](docs/img/supabase-tabelas.png)
```

### Arquivo `.env`

Crie `src/.env` a partir de `src/.env.example` e preencha com os seus dados:

```dotenv
SECRET_KEY='sua_chave_secreta_do_django'
DEBUG=False

# Supabase: Connect > Connection string
DATABASE_URL=postgresql://postgres.SEU_PROJECT_REF:SUA_SENHA@HOST_DO_POOLER:5432/postgres

SUPABASE_URL=https://SEU_PROJECT_REF.supabase.co
SUPABASE_KEY=sua_chave_publica_do_supabase

# Redis (use rediss:// se o seu Redis tiver TLS)
REDIS_URL=redis://default:SUA_SENHA@HOST_DO_REDIS:PORTA/0
```

> ⚠️ O arquivo `.env` contém senhas e está no `.gitignore`: **nunca o envie para o GitHub**. Para gerar a `SECRET_KEY`:
> `python -c "import secrets; print(secrets.token_urlsafe(50))"`

---

## ▶️ Como executar

Pré-requisitos: Python 3.10+, uma conta no Supabase (ou PostgreSQL local) e, opcionalmente, um Redis.

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar o ambiente
cd src
cp .env.example .env        # no Windows: copy .env.example .env  (depois preencha o .env)

# 3. Testar as conexões com Supabase e Redis
python teste_conexoes.py

# 4. Preparar o Django
python manage.py migrate

# 5. Criar tabelas, View, Function, Procedures e dados iniciais no banco
python manage.py configurar_banco

# 6. Criar o usuário de login
python manage.py createsuperuser

# 7. Rodar
python manage.py runserver
```

Acesse http://127.0.0.1:8000 e entre com o usuário criado.

> As tabelas são mapeadas pelo Django com `managed = False`, por isso o passo 5 (`configurar_banco`) deve ser executado antes de usar o sistema. Os scripts SQL equivalentes estão em `ddl/` e `dml/`.

### Como testar o Redis

```bash
python manage.py shell
```
```python
from django.core.cache import cache
cache.set("teste", "ok", 60)
print(cache.get("teste"))        # deve imprimir: ok
```
Na própria aplicação, use o menu **Painel Redis**. Também dá para ver as chaves pelo Redis Insight ou `redis-cli` (`KEYS gerente_notas*`).

---

## 🌐 Acesso online e vídeo

* **Sistema (Render):** https://gerente-notas.onrender.com/
  Usuário de teste: `Thiago` / senha `1234`. O plano gratuito pode demorar a carregar no primeiro acesso; use em computador.
* **Vídeo explicativo 1 (Joins):** https://drive.google.com/uc?id=1eb8qdmASeKHIpgChyErokfuOVIvIduei&export=download
* **Vídeo explicativo 2 (View, Function e Procedure):** https://drive.google.com/uc?id=1mN1ZJNC0kcW2UtfQB1gtx-7VSBX1ZtfH&export=download

---

## ✅ Requisitos do trabalho atendidos

* ✔ 1 View, 1 Function e 1 Procedure, com finalidades diferentes, criadas no banco e usadas pela aplicação
* ✔ 3 telas/funcionalidades usando os recursos (Relatório View, Média do aluno, Matricular aluno)
* ✔ Scripts de tabelas, inserts, View, Function e Procedure (`ddl/`, `dml/` e `configurar_banco`)
* ✔ Banco hospedado no Supabase e Redis para cache e sessões
* ✔ Repositório no GitHub, README e vídeo explicativo