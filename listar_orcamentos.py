import sqlite3


def listar_orcamentos():

    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            orcamentos.id,
            clientes.nome,
            clientes.telefone,
            orcamentos.servico,
            orcamentos.area,
            orcamentos.valor_m2,
            orcamentos.valor_total,
            orcamentos.status,
            orcamentos.data_criacao
        FROM orcamentos
        INNER JOIN clientes
        ON orcamentos.cliente_id = clientes.id
        ORDER BY orcamentos.id DESC
    """)

    orcamentos = cursor.fetchall()

    print("\n======= ORÇAMENTOS ========")

    if orcamentos:

        for orcamento in orcamentos:

            print(f"\nOrçamento: {orcamento[0]}")
            print(f"Cliente: {orcamento[1]}")
            print(f"Telefone: {orcamento[2]}")
            print(f"Serviço: {orcamento[3]}")
            print(f"Área: {orcamento[4]:.2f} m²")
            print(f"Valor por m²: R$ {orcamento[5]:.2f}")
            print(f"Valor total: R$ {orcamento[6]:.2f}")
            print(f"Status: {orcamento[7]}")
            print(f"Data: {orcamento[8]}")

            print("-" * 40)

    else:
        print("\nNenhum orçamento cadastrado.")

    conexao.close()