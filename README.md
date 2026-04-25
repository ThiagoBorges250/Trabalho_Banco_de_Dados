# 📚 Sistema Gerente de Notas

## 📌 Descrição

O **Sistema Gerente de Notas** é uma aplicação desenvolvida em **Python com Django**, integrada a um banco de dados **PostgreSQL**, com o objetivo de gerenciar informações acadêmicas como alunos, professores, disciplinas e matrículas.

O sistema permite realizar operações completas de CRUD (Cadastro, Consulta, Atualização e Exclusão), além de consultas complexas utilizando **JOINs**, conforme exigido na disciplina de Banco de Dados.

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido para atender aos requisitos da disciplina de **Banco de Dados**, aplicando conceitos de:

* Modelagem de banco relacional
* Uso de chaves primárias e estrangeiras
* Manipulação de dados (DDL, DML, DQL)
* Integração com aplicação externa (Django)

---

## 🛠 Tecnologias Utilizadas

* **Python 3**
* **Django**
* **PostgreSQL**
* **HTML / CSS**
* **Bootstrap**
* **Git e GitHub**

---

## 🧩 Funcionalidades do Sistema

* 🔐 Sistema de login
* 👨‍🎓 Cadastro de alunos
* 👨‍🏫 Cadastro de professores
* 📘 Cadastro de disciplinas
* 📝 Matrícula de alunos
* 📊 Lançamento de notas
* 🔄 Operações CRUD completas
* 🔍 Filtros e ordenação de dados
* 🔗 Consultas com INNER JOIN, LEFT JOIN e FULL OUTER JOIN
* 📈 Cálculo automático de média e status (Aprovado / Reprovado / Matriculado)

---

## 🗂 Estrutura do Projeto

```
gerente_notas/
│
├── diagrama/        # DER (Diagrama Entidade-Relacionamento)
├── ddl/             # Script de criação das tabelas
├── dml/             # Scripts de inserção, atualização e exclusão
├── dql/             # Consultas SQL (JOINs, filtros, ordenação)
├── src/             # Código fonte da aplicação Django
└── README.md        # Documentação do projeto
```

---

## 🗄️ Modelagem do Banco de Dados

O sistema possui as seguintes entidades principais:

* **Alunos**
* **Professores**
* **Disciplinas**
* **Matrículas**

Relacionamentos:

* Um professor pode ministrar várias disciplinas
* Um aluno pode se matricular em várias disciplinas
* A tabela matrícula conecta alunos e disciplinas

---

## 🖼️ Prints da Aplicação

### 🔐 Tela de Login

(INSERIR PRINT AQUI)

### 📋 Tela Principal

(INSERIR PRINT AQUI)

### 🔎 Consulta com JOIN

(INSERIR PRINT AQUI)

---

## ⚙️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/gerente_notas.git
```

---

### 2. Acessar o projeto

```bash
cd gerente_notas/src
```

---

### 3. Instalar dependências

```bash
pip install django psycopg2-binary
```

---

### 4. Configurar o banco de dados

No arquivo `settings.py`, configure:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gerente_notas',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### 5. Aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Criar usuário administrador

```bash
python manage.py createsuperuser
```

---

### 7. Executar o sistema

```bash
python manage.py runserver
```

Acesse:

```
http://127.0.0.1:8000/
```

---

## 🎥 Vídeo Demonstrativo

🔗 Link do vídeo:
(INSERIR LINK AQUI)

---

## 📊 Exemplos de Consultas (JOIN)

```sql
SELECT a.nome, d.nome_disciplina, m.nota
FROM matricula m
INNER JOIN alunos a ON m.fk_id_aluno = a.id_aluno
INNER JOIN disciplinas d ON m.fk_id_disciplina = d.id_disciplina;
```

---

## 📌 Requisitos Atendidos

✔ Banco com mais de 3 tabelas relacionadas
✔ Uso de PK e FK
✔ Scripts SQL organizados (DDL, DML, DQL)
✔ Aplicação com CRUD completo
✔ Uso de JOINs
✔ Interface gráfica (bônus)

---

## 👨‍💻 Autor

**Thiago Borges**

---

## 📩 Entrega

Projeto desenvolvido para a disciplina de **Banco de Dados**.
Professor: **Anderson Costa**

---
