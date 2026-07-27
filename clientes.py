from banco import conectar


# ======================================================
# CADASTRAR CLIENTE
# ======================================================

def cadastrar_cliente(nome, telefone):

    if not nome or not nome.strip():
        return False, "O nome do cliente é obrigatório."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes (
            nome,
            telefone
        )
        VALUES (?, ?)
    """, (
        nome.strip(),
        telefone.strip()
    ))

    conexao.commit()
    conexao.close()

    return True, "Cliente cadastrado com sucesso!"


# ======================================================
# LISTAR CLIENTES
# ======================================================

def listar_clientes():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            telefone
        FROM clientes
        ORDER BY nome
    """)

    clientes = cursor.fetchall()

    conexao.close()

    return clientes


# ======================================================
# BUSCAR CLIENTE POR ID
# ======================================================

def buscar_cliente(cliente_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            telefone
        FROM clientes
        WHERE id = ?
    """, (cliente_id,))

    cliente = cursor.fetchone()

    conexao.close()

    return cliente


# ======================================================
# EDITAR CLIENTE
# ======================================================

def editar_cliente(cliente_id, nome, telefone):

    if not nome or not nome.strip():
        return False, "O nome do cliente é obrigatório."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE clientes
        SET
            nome = ?,
            telefone = ?
        WHERE id = ?
    """, (
        nome.strip(),
        telefone.strip(),
        cliente_id
    ))

    conexao.commit()

    alterado = cursor.rowcount > 0

    conexao.close()

    if alterado:
        return True, "Cliente atualizado com sucesso!"

    return False, "Cliente não encontrado."


# ======================================================
# EXCLUIR CLIENTE
# ======================================================

def excluir_cliente(cliente_id):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            DELETE FROM clientes
            WHERE id = ?
        """, (cliente_id,))

        conexao.commit()

        if cursor.rowcount == 0:

            conexao.close()

            return False, "Cliente não encontrado."

        conexao.close()

        return True, "Cliente excluído com sucesso!"

    except Exception as erro:

        conexao.close()

        return False, (
            "Não foi possível excluir o cliente.\n"
            "Verifique se existem orçamentos vinculados a ele."
        )