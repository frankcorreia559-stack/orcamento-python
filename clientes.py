import sqlite3

from banco import conectar


# ==========================================================
# CADASTRAR CLIENTE
# ==========================================================

def cadastrar_cliente(
    usuario_id,
    nome,
    telefone="",
    email="",
    endereco=""
):

    if not usuario_id:

        return False, "Usuário não identificado."

    if not nome or not nome.strip():

        return False, "O nome do cliente é obrigatório."

    nome = nome.strip()

    telefone = (
        telefone.strip()
        if telefone
        else ""
    )

    email = (
        email.strip()
        if email
        else ""
    )

    endereco = (
        endereco.strip()
        if endereco
        else ""
    )


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO clientes (
                usuario_id,
                nome,
                telefone,
                email,
                endereco
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            usuario_id,
            nome,
            telefone,
            email,
            endereco
        ))

        conexao.commit()

        return (
            True,
            "Cliente cadastrado com sucesso!"
        )


    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao cadastrar cliente: {erro}"
        )

        return (
            False,
            "Não foi possível cadastrar o cliente."
        )


    finally:

        conexao.close()


# ==========================================================
# LISTAR CLIENTES
# ==========================================================

def listar_clientes(usuario_id):

    if not usuario_id:

        return []


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                nome,
                telefone,
                email,
                endereco,
                data_criacao

            FROM clientes

            WHERE usuario_id = ?

            ORDER BY nome COLLATE NOCASE
        """, (
            usuario_id,
        ))

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

def pesquisar_clientes(
    usuario_id,
    termo=""
):

    if not usuario_id:

        return []


    termo = (
        termo.strip()
        if termo
        else ""
    )


    if not termo:

        return listar_clientes(
            usuario_id
        )


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                nome,
                telefone,
                email,
                endereco,
                data_criacao

            FROM clientes

            WHERE usuario_id = ?

            AND (
                nome LIKE ?
                OR telefone LIKE ?
                OR email LIKE ?
            )

            ORDER BY nome COLLATE NOCASE
        """, (
            usuario_id,
            f"%{termo}%",
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

def buscar_cliente(
    usuario_id,
    cliente_id
):

    if not usuario_id:

        return None

    if not cliente_id:

        return None


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                nome,
                telefone,
                email,
                endereco,
                data_criacao

            FROM clientes

            WHERE id = ?

            AND usuario_id = ?
        """, (
            cliente_id,
            usuario_id
        ))

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

def editar_cliente(
    usuario_id,
    cliente_id,
    nome,
    telefone="",
    email="",
    endereco=""
):

    if not usuario_id:

        return (
            False,
            "Usuário não identificado."
        )


    if not cliente_id:

        return (
            False,
            "ID do cliente inválido."
        )


    if not nome or not nome.strip():

        return (
            False,
            "O nome do cliente é obrigatório."
        )


    nome = nome.strip()

    telefone = (
        telefone.strip()
        if telefone
        else ""
    )

    email = (
        email.strip()
        if email
        else ""
    )

    endereco = (
        endereco.strip()
        if endereco
        else ""
    )


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE clientes

            SET
                nome = ?,
                telefone = ?,
                email = ?,
                endereco = ?

            WHERE id = ?

            AND usuario_id = ?
        """, (
            nome,
            telefone,
            email,
            endereco,
            cliente_id,
            usuario_id
        ))


        if cursor.rowcount == 0:

            return (
                False,
                "Cliente não encontrado."
            )


        conexao.commit()

        return (
            True,
            "Cliente atualizado com sucesso!"
        )


    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao editar cliente: {erro}"
        )

        return (
            False,
            "Não foi possível atualizar o cliente."
        )


    finally:

        conexao.close()


# ==========================================================
# EXCLUIR CLIENTE
# ==========================================================

def excluir_cliente(
    usuario_id,
    cliente_id
):

    if not usuario_id:

        return (
            False,
            "Usuário não identificado."
        )


    if not cliente_id:

        return (
            False,
            "ID do cliente inválido."
        )


    conexao = conectar()

    try:

        cursor = conexao.cursor()


        # ==================================================
        # VERIFICAR SE O CLIENTE PERTENCE AO USUÁRIO
        # ==================================================

        cursor.execute("""
            SELECT id

            FROM clientes

            WHERE id = ?

            AND usuario_id = ?
        """, (
            cliente_id,
            usuario_id
        ))


        cliente = cursor.fetchone()


        if not cliente:

            return (
                False,
                "Cliente não encontrado."
            )


        # ==================================================
        # EXCLUIR CLIENTE
        # ==================================================

        cursor.execute("""
            DELETE FROM clientes

            WHERE id = ?

            AND usuario_id = ?
        """, (
            cliente_id,
            usuario_id
        ))


        conexao.commit()


        return (
            True,
            "Cliente excluído com sucesso!"
        )


    except sqlite3.IntegrityError as erro:

        conexao.rollback()

        print(
            f"Erro de integridade ao excluir cliente: {erro}"
        )

        return (
            False,
            "Não foi possível excluir o cliente."
        )


    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao excluir cliente: {erro}"
        )

        return (
            False,
            "Ocorreu um erro ao excluir o cliente."
        )


    finally:

        conexao.close()


# ==========================================================
# CONTAR CLIENTES
# ==========================================================

def contar_clientes(
    usuario_id
):

    if not usuario_id:

        return 0


    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)

            FROM clientes

            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))

        resultado = cursor.fetchone()

        return resultado[0]


    except sqlite3.Error as erro:

        print(
            f"Erro ao contar clientes: {erro}"
        )

        return 0


    finally:

        conexao.close()