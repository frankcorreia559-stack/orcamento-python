import sqlite3


def excluir_orcamento():

    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    print("\n======= EXCLUIR ORÇAMENTO ========")

    # Buscar orçamentos cadastrados
    cursor.execute("""
        SELECT
            orcamentos.id,
            clientes.nome,
            orcamentos.servico,
            orcamentos.valor_total,
            orcamentos.status
        FROM orcamentos
        INNER JOIN clientes
        ON orcamentos.cliente_id = clientes.id
        ORDER BY orcamentos.id
    """)

    orcamentos = cursor.fetchall()

    if not orcamentos:
        print("\nNenhum orçamento cadastrado.")
        conexao.close()
        return

    # Mostrar orçamentos
    print("\n======= ORÇAMENTOS CADASTRADOS ========")

    for orcamento in orcamentos:
        print(
            f"ID: {orcamento[0]} | "
            f"Cliente: {orcamento[1]} | "
            f"Serviço: {orcamento[2]} | "
            f"Total: R$ {orcamento[3]:.2f} | "
            f"Status: {orcamento[4]}"
        )

    # Escolher orçamento
    try:
        orcamento_id = int(
            input("\nDigite o ID do orçamento que deseja excluir: ")
        )
    except ValueError:
        print("\nID inválido.")
        conexao.close()
        return

    # Buscar orçamento selecionado
    cursor.execute("""
        SELECT
            orcamentos.id,
            clientes.nome,
            orcamentos.servico,
            orcamentos.valor_total
        FROM orcamentos
        INNER JOIN clientes
        ON orcamentos.cliente_id = clientes.id
        WHERE orcamentos.id = ?
    """, (orcamento_id,))

    orcamento = cursor.fetchone()

    if orcamento is None:
        print("\nOrçamento não encontrado.")
        conexao.close()
        return

    # Mostrar dados antes de excluir
    print("\n======= ORÇAMENTO SELECIONADO ========")
    print(f"ID: {orcamento[0]}")
    print(f"Cliente: {orcamento[1]}")
    print(f"Serviço: {orcamento[2]}")
    print(f"Valor total: R$ {orcamento[3]:.2f}")

    # Confirmação
    confirmacao = input(
        "\nTem certeza que deseja excluir este orçamento? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("\nExclusão cancelada.")
        conexao.close()
        return

    # Excluir orçamento
    cursor.execute("""
        DELETE FROM orcamentos
        WHERE id = ?
    """, (orcamento_id,))

    conexao.commit()
    conexao.close()

    print("\nOrçamento excluído com sucesso!")