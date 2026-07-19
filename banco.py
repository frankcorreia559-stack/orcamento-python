import sqlite3

conexao = sqlite3.connect("orcamentos.db")
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
    cliente_id INTEGER,
    servico TEXT,
    area REAL,
    valor_m2 REAL,
    valor_total REAL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")