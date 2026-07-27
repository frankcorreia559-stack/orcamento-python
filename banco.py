import sqlite3


NOME_BANCO = "orcamentos.db"


def conectar():
    conexao = sqlite3.connect(NOME_BANCO)

    # Ativa o uso de chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():

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
            ON DELETE RESTRICT
            ON UPDATE CASCADE
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":

    criar_tabelas()

    print("Banco de dados configurado com sucesso!")