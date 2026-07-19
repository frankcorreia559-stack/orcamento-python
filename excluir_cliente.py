import sqlite3

def excluir_cliente():
    
    conexao = sqlite3.connect('orcamentos.db')
    cursor = conexao.cursor()

    id_cliente = int(input('ID do cliente:'))

    cursor.execute("""
                   DELETE FROM clientes
                   WHERE id = ?
                   """,(id_cliente,)
                   )
    
    conexao.commit()

    if cursor.rowcount > 0:
        print('Cliente excluido com sucesso!')

    else:
        print('Cliente nao encontrado!')    


    conexao.close()

    