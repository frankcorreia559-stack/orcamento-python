import sqlite3

def editar_cliente():

    conexao = sqlite3.connect('orcamentos.db')
    cursor = conexao.cursor()

    id_cliente = int(input('ID do cliente: '))
    nome = input('Novo nome: ')
    telefone = input('Novo telefone: ')

    cursor.execute("""
                   UPDATE clientes 
                   SET nome = ?, telefone = ?
                   WHERE id = ?
                   """, (nome, telefone, id_cliente)
                   )
    

    conexao.commit()

    if cursor.rowcount > 0:
        print('Cliente atualizado com sucesso!')

    else:
        print('Cliente não cadastrado!')  

    conexao.close()      