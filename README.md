# OrçaSmart

Sistema de gestão de orçamentos desenvolvido para facilitar o controle de clientes, serviços e orçamentos de empresas do setor de gesso e drywall.

O projeto nasceu a partir de uma necessidade real de organizar o processo de criação e gerenciamento de orçamentos, transformando uma atividade que inicialmente era realizada de forma manual em um sistema digital.

---

## 📌 Sobre o projeto

O **OrçaSmart** é uma aplicação desenvolvida em Python com foco em:

* Cadastro de clientes
* Gerenciamento de orçamentos
* Cálculo de valores
* Organização de serviços
* Armazenamento de dados
* Geração de documentos
* Interface gráfica
* Organização das informações da empresa

O projeto também foi utilizado como projeto prático de estudo para desenvolver conhecimentos em **Python, banco de dados, Git, GitHub, interfaces gráficas e arquitetura de software**.

---

## 🎯 Objetivo

O objetivo do OrçaSmart é tornar o processo de elaboração e gerenciamento de orçamentos mais rápido, organizado e confiável.

A aplicação busca reduzir tarefas manuais e centralizar as principais informações utilizadas durante o atendimento ao cliente.

---

## 🚀 Funcionalidades

### 👤 Clientes

* Cadastro de clientes
* Listagem de clientes
* Edição de informações
* Exclusão de clientes
* Armazenamento dos dados em banco de dados

### 📋 Orçamentos

* Cadastro de orçamento
* Seleção do cliente
* Registro do serviço
* Registro da quantidade/metragem
* Definição do valor por unidade
* Cálculo do valor total
* Listagem de orçamentos

### 📊 Relatórios

Estrutura preparada para futuras funcionalidades de relatórios e análise dos dados cadastrados.

### 📄 Geração de PDF

O sistema possui integração com geração de documentos PDF para transformar os dados do orçamento em um documento apresentável ao cliente.

---

## 🛠️ Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

| Tecnologia    | Utilização           |
| ------------- | -------------------- |
| Python        | Linguagem principal  |
| SQLite        | Banco de dados       |
| Tkinter       | Interface gráfica    |
| CustomTkinter | Interface moderna    |
| ReportLab     | Geração de PDF       |
| Git           | Controle de versão   |
| GitHub        | Hospedagem do código |

---

## 🗂️ Estrutura do projeto

Uma das estruturas utilizadas durante o desenvolvimento foi:

```text
OrçaSmart/
│
├── backend/
│
├── database/
│
├── interface.py
├── banco.py
├── cadastrar_cliente.py
├── listar_cliente.py
├── cadastrar_orcamento.py
├── listar_orcamento.py
├── gerar_pdf.py
├── principal.py
│
├── logo_orcamento.png
├── orcamentos.db
│
├── README.md
└── requirements.txt
```

A estrutura pode sofrer alterações conforme o projeto evolui.

---

## 🗄️ Banco de dados

O OrçaSmart utiliza **SQLite** para armazenamento local dos dados.

Entre as informações armazenadas estão:

### Clientes

```text
id
nome
telefone
```

### Orçamentos

```text
id
cliente
serviço
metragem
valor_m²
valor_total
```

O banco de dados permite que as informações permaneçam armazenadas mesmo após o encerramento da aplicação.

---

## 💻 Instalação

### 1. Clone o repositório

```bash
git clone SEU_LINK_DO_REPOSITORIO
```

### 2. Entre na pasta

```bash
cd orcasmart
```

### 3. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute o sistema

```bash
python principal.py
```

---

## 🔐 Boas práticas

Durante o desenvolvimento do projeto foram aplicados conceitos importantes de desenvolvimento de software, como:

* Separação de responsabilidades
* Organização por módulos
* Persistência de dados
* Controle de versão
* Tratamento de erros
* Validação de informações
* Uso de ambiente virtual
* Organização de dependências

---

## 📚 O que este projeto demonstra

O OrçaSmart representa a aplicação prática de conhecimentos adquiridos durante os estudos de desenvolvimento de sistemas.

Entre os principais conhecimentos envolvidos estão:

**Python**

* Funções
* Classes
* Programação Orientada a Objetos
* Manipulação de arquivos
* Tratamento de exceções
* Bibliotecas externas

**Banco de dados**

* SQLite
* SQL
* CRUD
* Relacionamento entre dados
* Persistência

**Git e GitHub**

* Commits
* Branches
* Push
* Pull
* Versionamento
* Organização de repositório

**Interface**

* Tkinter
* CustomTkinter
* Organização de telas
* Componentização

---

## 🔄 Evolução do projeto

O OrçaSmart começou como uma aplicação simples para criação de orçamentos e foi evoluindo gradualmente.

### Versão inicial

* Cadastro de serviços
* Cálculo de valores
* Salvamento em arquivos JSON

### Evolução

* Banco de dados SQLite
* Cadastro de clientes
* Cadastro de orçamentos
* Interface gráfica
* Geração de PDF
* Organização do projeto

### Próximas etapas

* [ ] Dashboard com indicadores
* [ ] Sistema de login
* [ ] Controle de usuários
* [ ] Relatórios financeiros
* [ ] Histórico de orçamentos
* [ ] Exportação de dados
* [ ] Backup automático
* [ ] API REST
* [ ] Aplicação web
* [ ] Aplicativo mobile

---

## 📸 Interface

Adicione aqui imagens da aplicação:

```text
docs/
├── dashboard.png
├── clientes.png
├── orcamentos.png
└── relatorios.png
```

Exemplo:

```markdown
![Dashboard](docs/dashboard.png)
```

---

## 🧠 Aprendizado

O OrçaSmart foi desenvolvido como um projeto prático para transformar conhecimentos teóricos em uma aplicação real.

Durante o desenvolvimento foram trabalhados conceitos de:

```text
Python
   ↓
Programação Orientada a Objetos
   ↓
Banco de Dados
   ↓
CRUD
   ↓
Interface Gráfica
   ↓
Geração de PDF
   ↓
Git
   ↓
GitHub
```

---

## 🔮 Futuro do OrçaSmart

A ideia é transformar o OrçaSmart em uma solução cada vez mais completa para gerenciamento de empresas que trabalham com serviços e orçamentos.

A evolução planejada inclui uma arquitetura baseada em API, aplicação web, autenticação de usuários, dashboard, relatórios e possibilidade de acesso aos dados de diferentes dispositivos.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido como projeto prático de estudos e evolução em desenvolvimento de software.

**Desenvolvedor:** Frank Correia

---

## 📄 Licença

Este projeto pode receber uma licença específica conforme sua finalidade e forma de distribuição.

---

## ⭐ Contribuição

Sugestões e melhorias são bem-vindas.

Se você encontrar algum problema ou tiver uma ideia para melhorar o projeto, abra uma **Issue** ou envie uma proposta de alteração.

---

## 📌 Status

🚧 **Em desenvolvimento**

O projeto continua evoluindo conforme novos conhecimentos e funcionalidades são adicionados.
