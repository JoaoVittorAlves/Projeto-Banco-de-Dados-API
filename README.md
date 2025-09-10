## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

* **Python:** (Versão 3.10 ou superior). Você pode baixar em [python.org](https://python.org). Durante a instalação no Windows, marque a caixa "Add Python to PATH".
* **PostgreSQL:** O sistema de gerenciamento de banco de dados. Você pode baixar em [postgresql.org](https://www.postgresql.org/download/). **Anote a senha** que você definir para o superusuário `postgres` durante a instalação.
* **Git:** Para clonar o repositório. Você pode baixar em [git-scm.com](https://git-scm.com/).
* **Um Cliente de Banco de Dados:** O [pgAdmin](https://www.pgadmin.org/) geralmente é instalado junto com o PostgreSQL e será útil para visualizar o banco de dados.

## Configuração do Ambiente (Passo a Passo)

Siga estes passos para configurar o ambiente de desenvolvimento localmente.

### 1. Clonar o Repositório

Abra um terminal (PowerShell, CMD, ou Git Bash) e clone este repositório para a sua máquina:

```bash
git clone https://github.com/JoaoVittorAlves/Projeto-Banco-de-Dados-API.git
cd Projeto-Banco-de-Dados-API
```

### 2. Configurar o Banco de Dados PostgreSQL

A aplicação precisa de um banco de dados para armazenar os dados.

1.  **Abra o pgAdmin**.
2.  Conecte-se ao seu servidor PostgreSQL local.
3.  No painel esquerdo, clique com o botão direito em **"Databases"** e selecione **Create -> Database...**.
4.  Dê o nome ao banco de dados de `clinica_db` e clique em **Save**.
5.  Clique no banco `clinica_db` recém-criado, vá ao menu **Tools -> Query Tool**.
6.  Abra o arquivo `.sql` do projeto, copie todo o seu conteúdo, cole na Query Tool e execute (clicando no ícone de "play"). Isso criará todas as tabelas e relacionamentos necessários.

### 3. Criar e Ativar o Ambiente Virtual

```powershell
# 1. Crie o ambiente virtual (será criada uma pasta 'venv')
python -m venv venv

# 2. Ative o ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 4. Instalar as Dependências

Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:

```
fastapi[all]
sqlalchemy
psycopg2-binary
python-dotenv
```

Agora, com o ambiente virtual ativado, instale todas as bibliotecas necessárias com um único comando:

```bash
pip install -r requirements.txt
```

### 5. Configurar as Variáveis de Ambiente

A aplicação precisa saber como se conectar ao seu banco de dados.

1.  Na **raiz do projeto**, crie um arquivo chamado `.env`.
2.  Abra o arquivo `.env` e adicione a seguinte linha, substituindo `SUA_SENHA` pela senha do seu usuário `postgres`:

```
DATABASE_URL="postgresql://postgres:SUA_SENHA@localhost:5432/clinica_db"
```
## Executando a Aplicação

Com tudo configurado, você pode iniciar o servidor da API.

1.  Certifique-se de que seu ambiente virtual `(venv)` está ativado.
2.  Certifique-se de que você está na **pasta raiz** do projeto.
3.  Execute o seguinte comando:

```bash
uvicorn main.main:app --reload
```
O terminal deverá exibir uma mensagem indicando que o servidor está rodando em `http://127.0.0.1:8000`.

## Como Usar e Testar a API

A maneira mais fácil de interagir com a API é através da documentação interativa gerada automaticamente pelo FastAPI.

1.  Abra seu navegador de internet.
2.  Acesse a URL: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Nesta página, você poderá ver todos os endpoints disponíveis, expandi-los, preencher os dados e clicar em "Execute" para testar cada uma das operações CRUD (Inserir, Alterar, Pesquisar, Remover, etc.) diretamente do navegador, conforme requerido pelas especificações do projeto.