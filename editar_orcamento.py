import sqlite3


def editar_orcamento():

    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    print("\n======= EDITAR ORÇAMENTO ========")

    # Listar os orçamentos existentes
    cursor.execute("""
        SELECT
            orcamentos.id,
            clientes.nome,
            orcamentos.servico,
            orcamentos.area,
            orcamentos.valor_m2,
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
            f"Total: R$ {orcamento[5]:.2f} | "
            f"Status: {orcamento[6]}"
        )

    # Escolher orçamento
    try:
        orcamento_id = int(
            input("\nDigite o ID do orçamento que deseja editar: ")
        )
    except ValueError:
        print("\nID inválido.")
        conexao.close()
        return

    # Buscar orçamento selecionado
    cursor.execute("""
        SELECT
            cliente_id,
            servico,
            area,
            valor_m2,
            status
        FROM orcamentos
        WHERE id = ?
    """, (orcamento_id,))

    orcamento_atual = cursor.fetchone()

    if orcamento_atual is None:
        print("\nOrçamento não encontrado.")
        conexao.close()
        return

    # Dados atuais
    cliente_id = orcamento_atual[0]
    servico_atual = orcamento_atual[1]
    area_atual = orcamento_atual[2]
    valor_m2_atual = orcamento_atual[3]
    status_atual = orcamento_atual[4]

    print("\n======= DADOS ATUAIS ========")
    print(f"Serviço: {servico_atual}")
    print(f"Área: {area_atual:.2f} m²")
    print(f"Valor por m²: R$ {valor_m2_atual:.2f}")
    print(f"Status: {status_atual}")

    print("\nPressione ENTER para manter o valor atual.")

    # Novo serviço
    novo_servico = input(
        f"Serviço [{servico_atual}]: "
    ).strip()

    if not novo_servico:
        novo_servico = servico_atual

    # Nova área
    nova_area_input = input(
        f"Área em m² [{area_atual}]: "
    ).strip()

    if nova_area_input:
        try:
            nova_area = float(nova_area_input)
        except ValueError:
            print("\nÁrea inválida.")
            conexao.close()
            return
    else:
        nova_area = area_atual

    # Novo valor por m²
    novo_valor_m2_input = input(
        f"Valor do m² [R$ {valor_m2_atual:.2f}]: "
    ).strip()

    if novo_valor_m2_input:
        try:
            novo_valor_m2 = float(novo_valor_m2_input)
        except ValueError:
            print("\nValor do m² inválido.")
            conexao.close()
            return
    else:
        novo_valor_m2 = valor_m2_atual

    # Novo status
    novo_status = input(
        f"Status [{status_atual}] "
        "(Pendente/Aprovado/Recusado): "
    ).strip()

    if not novo_status:
        novo_status = status_atual

    # Recalcular valor total
    novo_valor_total = nova_area * novo_valor_m2

    # Atualizar banco
    cursor.execute("""
        UPDATE orcamentos
        SET
            servico = ?,
            area = ?,
            valor_m2 = ?,
            valor_total = ?,
            status = ?
        WHERE id = ?
    """, (
        novo_servico,
        nova_area,
        novo_valor_m2,
        novo_valor_total,
        novo_status,
        orcamento_id
    ))

    conexao.commit()
    conexao.close()

    print("\n======= ORÇAMENTO ATUALIZADO ========")
    print(f"Serviço: {novo_servico}")
    print(f"Área: {nova_area:.2f} m²")
    print(f"Valor por m²: R$ {novo_valor_m2:.2f}")
    print(f"Valor total: R$ {novo_valor_total:.2f}")
    print(f"Status: {novo_status}")