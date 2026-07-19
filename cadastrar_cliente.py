import sqlite3

def cadastrar_cliente():
    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")

    cursor.execute("""
    INSERT INTO clientes (nome, telefone)
    VALUES (?, ?)
    """, (nome, telefone))

    conexao.commit()
    conexao.close()

    print("Cliente cadastrado com sucesso!")