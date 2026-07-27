import sqlite3


def cadastrar_orcamento():

    conexao = sqlite3.connect("orcamentos.db")
    cursor = conexao.cursor()

    print("\n======= NOVO ORÇAMENTO ========")

    # Buscar clientes cadastrados
    cursor.execute("""
        SELECT id, nome, telefone
        FROM clientes
        ORDER BY nome
    """)

    clientes = cursor.fetchall()

    if not clientes:
        print("\nNenhum cliente cadastrado.")
        print("Cadastre um cliente antes de criar um orçamento.")

        conexao.close()
        return

    # Mostrar clientes
    print("\n======= CLIENTES CADASTRADOS ========")

    for cliente in clientes:
        print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Telefone: {cliente[2]}")

    # Escolher cliente
    try:
        cliente_id = int(input("\nDigite o ID do cliente: "))
    except ValueError:
        print("\nID inválido.")
        conexao.close()
        return

    # Verificar se o cliente existe
    cursor.execute("""
        SELECT id, nome
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    cliente = cursor.fetchone()

    if cliente is None:
        print("\nCliente não encontrado.")
        conexao.close()
        return

    print(f"\nCliente selecionado: {cliente[1]}")

    # Dados do orçamento
    servico = input("Serviço: ")

    try:
        area = float(input("Área em m²: "))
        valor_m2 = float(input("Valor do m²: "))
    except ValueError:
        print("\nDigite valores numéricos válidos.")
        conexao.close()
        return

    # Calcular valor total
    valor_total = area * valor_m2

    # Salvar orçamento
    cursor.execute("""
        INSERT INTO orcamentos
        (cliente_id, servico, area, valor_m2, valor_total)
        VALUES (?, ?, ?, ?, ?)
    """, (
        cliente_id,
        servico,
        area,
        valor_m2,
        valor_total
    ))

    conexao.commit()
    conexao.close()

    print("\n======= ORÇAMENTO CADASTRADO ========")
    print(f"Cliente: {cliente[1]}")
    print(f"Serviço: {servico}")
    print(f"Área: {area:.2f} m²")
    print(f"Valor por m²: R$ {valor_m2:.2f}")
    print(f"Valor total: R$ {valor_total:.2f}")