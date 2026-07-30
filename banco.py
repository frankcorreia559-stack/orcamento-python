import sqlite3


BANCO = "orcamentos.db"


def conectar():

    conexao = sqlite3.connect(BANCO)

    # Permite acessar os dados pelo nome da coluna
    # Exemplo: orcamento["cliente_nome"]
    conexao.row_factory = sqlite3.Row

    return conexao


def inicializar_banco():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            telefone TEXT

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orcamentos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            cliente_id INTEGER NOT NULL,

            servico TEXT NOT NULL,

            area REAL NOT NULL,

            valor_m2 REAL NOT NULL,

            valor_total REAL NOT NULL,

            status TEXT DEFAULT 'Pendente',

            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (cliente_id)
            REFERENCES clientes(id)

        )
    """)

    conexao.commit()

    conexao.close()