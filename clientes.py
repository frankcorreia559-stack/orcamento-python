import sqlite3

from banco import conectar


# ==========================================================
# CADASTRAR CLIENTE
# ==========================================================

def cadastrar_cliente(nome, telefone=""):
    """
    Cadastra um novo cliente.

    Retorna:
        (True, mensagem) em caso de sucesso.
        (False, mensagem) em caso de erro.
    """

    # ------------------------------------------------------
    # VALIDAÇÃO
    # ------------------------------------------------------

    if not nome or not nome.strip():
        return False, "O nome do cliente é obrigatório."

    # ------------------------------------------------------
    # LIMPEZA DOS DADOS
    # ------------------------------------------------------

    nome = nome.strip()
    telefone = telefone.strip() if telefone else ""

    # ------------------------------------------------------
    # CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # --------------------------------------------------
        # INSERIR CLIENTE
        # --------------------------------------------------

        cursor.execute("""
            INSERT INTO clientes (
                nome,
                telefone
            )
            VALUES (?, ?)
        """, (
            nome,
            telefone
        ))

        conexao.commit()

        return True, "Cliente cadastrado com sucesso!"

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao cadastrar cliente: {erro}"
        )

        return False, (
            "Não foi possível cadastrar o cliente."
        )

    finally:

        conexao.close()


# ==========================================================
# LISTAR CLIENTES
# ==========================================================

def listar_clientes():
    """
    Retorna todos os clientes cadastrados.
    """

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                telefone
            FROM clientes
            ORDER BY nome COLLATE NOCASE
        """)

        return cursor.fetchall()

    except sqlite3.Error as erro:

        print(
            f"Erro ao listar clientes: {erro}"
        )

        return []

    finally:

        conexao.close()


# ==========================================================
# PESQUISAR CLIENTES
# ==========================================================

def pesquisar_clientes(termo):
    """
    Pesquisa clientes pelo nome ou telefone.

    Se o termo estiver vazio, retorna todos os clientes.
    """

    # ------------------------------------------------------
    # LIMPAR TERMO DE PESQUISA
    # ------------------------------------------------------

    termo = termo.strip() if termo else ""

    # ------------------------------------------------------
    # PESQUISA VAZIA
    # ------------------------------------------------------

    if not termo:
        return listar_clientes()

    # ------------------------------------------------------
    # CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                telefone
            FROM clientes
            WHERE nome LIKE ?
               OR telefone LIKE ?
            ORDER BY nome COLLATE NOCASE
        """, (
            f"%{termo}%",
            f"%{termo}%"
        ))

        return cursor.fetchall()

    except sqlite3.Error as erro:

        print(
            f"Erro ao pesquisar clientes: {erro}"
        )

        return []

    finally:

        conexao.close()


# ==========================================================
# BUSCAR CLIENTE POR ID
# ==========================================================

def buscar_cliente(cliente_id):
    """
    Busca um cliente específico pelo ID.

    Retorna:
        sqlite3.Row se encontrado.
        None caso não exista.
    """

    # ------------------------------------------------------
    # VALIDAR ID
    # ------------------------------------------------------

    if not cliente_id:
        return None

    # ------------------------------------------------------
    # CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                telefone
            FROM clientes
            WHERE id = ?
        """, (cliente_id,))

        return cursor.fetchone()

    except sqlite3.Error as erro:

        print(
            f"Erro ao buscar cliente: {erro}"
        )

        return None

    finally:

        conexao.close()


# ==========================================================
# EDITAR CLIENTE
# ==========================================================

def editar_cliente(cliente_id, nome, telefone=""):
    """
    Atualiza os dados de um cliente existente.
    """

    # ------------------------------------------------------
    # VALIDAÇÕES
    # ------------------------------------------------------

    if not nome or not nome.strip():
        return False, "O nome do cliente é obrigatório."

    if not cliente_id:
        return False, "ID do cliente inválido."

    # ------------------------------------------------------
    # LIMPEZA DOS DADOS
    # ------------------------------------------------------

    nome = nome.strip()
    telefone = telefone.strip() if telefone else ""

    # ------------------------------------------------------
    # CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # --------------------------------------------------
        # ATUALIZAR CLIENTE
        # --------------------------------------------------

        cursor.execute("""
            UPDATE clientes
            SET
                nome = ?,
                telefone = ?
            WHERE id = ?
        """, (
            nome,
            telefone,
            cliente_id
        ))

        # --------------------------------------------------
        # VERIFICAR SE O CLIENTE EXISTE
        # --------------------------------------------------

        if cursor.rowcount == 0:

            return False, "Cliente não encontrado."

        conexao.commit()

        return True, (
            "Cliente atualizado com sucesso!"
        )

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao editar cliente: {erro}"
        )

        return False, (
            "Não foi possível atualizar o cliente."
        )

    finally:

        conexao.close()


# ==========================================================
# EXCLUIR CLIENTE
# ==========================================================

def excluir_cliente(cliente_id):
    """
    Exclui um cliente pelo ID.

    O banco impede a exclusão caso existam
    orçamentos vinculados ao cliente.
    """

    # ------------------------------------------------------
    # VALIDAR ID
    # ------------------------------------------------------

    if not cliente_id:
        return False, "ID do cliente inválido."

    # ------------------------------------------------------
    # CONEXÃO COM O BANCO
    # ------------------------------------------------------

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # --------------------------------------------------
        # EXCLUIR CLIENTE
        # --------------------------------------------------

        cursor.execute("""
            DELETE FROM clientes
            WHERE id = ?
        """, (cliente_id,))

        # --------------------------------------------------
        # VERIFICAR SE O CLIENTE EXISTE
        # --------------------------------------------------

        if cursor.rowcount == 0:

            return False, "Cliente não encontrado."

        conexao.commit()

        return True, (
            "Cliente excluído com sucesso!"
        )

    # ------------------------------------------------------
    # CLIENTE POSSUI ORÇAMENTOS
    # ------------------------------------------------------

    except sqlite3.IntegrityError:

        conexao.rollback()

        return False, (
            "Não foi possível excluir o cliente.\n"
            "Existem orçamentos vinculados a este cliente."
        )

    # ------------------------------------------------------
    # OUTROS ERROS DO SQLITE
    # ------------------------------------------------------

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao excluir cliente: {erro}"
        )

        return False, (
            "Ocorreu um erro ao excluir o cliente."
        )

    finally:

        conexao.close()