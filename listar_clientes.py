import sqlite3

def listar_clientes():
    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n===== LISTA DE CLIENTES =====")

    if clientes:
        for cliente in clientes:
            print(f"ID: {cliente[0]}")
            print(f"Nome: {cliente[1]}")
            print(f"Telefone: {cliente[2]}")
            print("-" * 23)
    else:
        print("Nenhum cliente cadastrado.")

    conexao.close()