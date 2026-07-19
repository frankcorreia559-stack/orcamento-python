import sqlite3

def listar_orcamentos():

    conexao = sqlite3.connect('orcamento.db')
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT
       orcamentos.id,
       clientes.nome,
       orcamentos.servico,
       orcamentos.area,
       orcamentos.valor_m2,
       orcamentos.valor_total
    FROM orcamentos
    JOIN clientes
    ON orcamentos.cliente_id = clientes.id
    """)

    orcamento =cursor.fetchall()

    print('\n======ORÇAMENTOS======')

    if orcamento:
        for orcamentos in orcamento:
            print(f"Orçamento: {orcamentos[0]}")
            print(f"Cliente: {orcamentos[1]}")
            print(f"Serviço: {orcamentos[2]}")
            print(f"Área: {orcamentos[3]} m²")
            print(f"Valor m²: R$ {orcamentos[4]:.2f}")
            print(f"Total: R$ {orcamentos[5]:.2f}")
            print("-" * 30)
    else:
        print('Nenhum orçamento cadastrado.') 

    conexao.close()           