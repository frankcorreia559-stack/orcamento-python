import sqlite3
import hashlib


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

BANCO = "orcamentos.db"


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

def conectar():

    conexao = sqlite3.connect(
        BANCO
    )

    conexao.row_factory = sqlite3.Row

    return conexao


# ==========================================================
# CRIAR TABELA DE USUÁRIOS
# ==========================================================

def criar_tabela_usuarios():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            usuario TEXT NOT NULL UNIQUE,

            senha TEXT NOT NULL,

            data_criacao TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conexao.commit()

    conexao.close()


# ==========================================================
# CRIPTOGRAFAR SENHA
# ==========================================================

def criptografar_senha(senha):

    return hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()


# ==========================================================
# CRIAR CONTA
# ==========================================================

def criar_conta(
    nome,
    usuario,
    senha
):

    # ------------------------------------------------------
    # LIMPAR ESPAÇOS
    # ------------------------------------------------------

    nome = nome.strip()

    usuario = usuario.strip()

    senha = senha.strip()

    # ------------------------------------------------------
    # VALIDAR NOME
    # ------------------------------------------------------

    if not nome:

        return (
            False,
            "Digite o nome completo."
        )

    # ------------------------------------------------------
    # VALIDAR USUÁRIO
    # ------------------------------------------------------

    if not usuario:

        return (
            False,
            "Digite um nome de usuário."
        )

    # ------------------------------------------------------
    # VALIDAR SENHA
    # ------------------------------------------------------

    if not senha:

        return (
            False,
            "Digite uma senha."
        )

    # ------------------------------------------------------
    # TAMANHO DA SENHA
    # ------------------------------------------------------

    if len(senha) < 4:

        return (
            False,
            "A senha deve ter pelo menos 4 caracteres."
        )

    # ------------------------------------------------------
    # CRIAR TABELA
    # ------------------------------------------------------

    criar_tabela_usuarios()

    # ------------------------------------------------------
    # CRIPTOGRAFAR SENHA
    # ------------------------------------------------------

    senha_hash = criptografar_senha(
        senha
    )

    # ------------------------------------------------------
    # SALVAR NO BANCO
    # ------------------------------------------------------

    conexao = None

    try:

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios
            (
                nome,
                usuario,
                senha
            )
            VALUES (?, ?, ?)
        """, (
            nome,
            usuario,
            senha_hash
        ))

        conexao.commit()

        return (
            True,
            "Conta criada com sucesso!"
        )

    except sqlite3.IntegrityError:

        return (
            False,
            "Esse nome de usuário já está cadastrado."
        )

    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao criar conta: {erro}"
        )

    finally:

        if conexao:

            conexao.close()


# ==========================================================
# AUTENTICAR USUÁRIO
# ==========================================================

def autenticar_usuario(
    usuario,
    senha
):

    # ------------------------------------------------------
    # LIMPAR ESPAÇOS
    # ------------------------------------------------------

    usuario = usuario.strip()

    senha = senha.strip()

    # ------------------------------------------------------
    # VALIDAR CAMPOS
    # ------------------------------------------------------

    if not usuario or not senha:

        return (
            False,
            None
        )

    # ------------------------------------------------------
    # CRIPTOGRAFAR SENHA DIGITADA
    # ------------------------------------------------------

    senha_hash = criptografar_senha(
        senha
    )

    conexao = None

    try:

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                usuario,
                data_criacao

            FROM usuarios

            WHERE usuario = ?

            AND senha = ?
        """, (
            usuario,
            senha_hash
        ))

        resultado = cursor.fetchone()

        # --------------------------------------------------
        # USUÁRIO NÃO ENCONTRADO
        # --------------------------------------------------

        if resultado is None:

            return (
                False,
                None
            )

        # --------------------------------------------------
        # CONVERTER SQLITE ROW PARA DICT
        # --------------------------------------------------

        dados_usuario = dict(
            resultado
        )

        return (
            True,
            dados_usuario
        )

    except sqlite3.Error as erro:

        print(
            f"Erro ao autenticar usuário: {erro}"
        )

        return (
            False,
            None
        )

    finally:

        if conexao:

            conexao.close()


# ==========================================================
# BUSCAR USUÁRIO POR ID
# ==========================================================

def buscar_usuario_por_id(
    id_usuario
):

    conexao = None

    try:

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                usuario,
                data_criacao

            FROM usuarios

            WHERE id = ?
        """, (
            id_usuario,
        ))

        resultado = cursor.fetchone()

        if resultado is None:

            return None

        return dict(
            resultado
        )

    except sqlite3.Error as erro:

        print(
            f"Erro ao buscar usuário: {erro}"
        )

        return None

    finally:

        if conexao:

            conexao.close()


# ==========================================================
# LISTAR USUÁRIOS
# ==========================================================

def listar_usuarios():

    conexao = None

    try:

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                usuario,
                data_criacao

            FROM usuarios

            ORDER BY id DESC
        """)

        resultados = cursor.fetchall()

        return [
            dict(usuario)
            for usuario in resultados
        ]

    except sqlite3.Error as erro:

        print(
            f"Erro ao listar usuários: {erro}"
        )

        return []

    finally:

        if conexao:

            conexao.close()


# ==========================================================
# EXCLUIR USUÁRIO
# ==========================================================

def excluir_usuario(
    id_usuario
):

    conexao = None

    try:

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM usuarios

            WHERE id = ?
        """, (
            id_usuario,
        ))

        conexao.commit()

        if cursor.rowcount == 0:

            return (
                False,
                "Usuário não encontrado."
            )

        return (
            True,
            "Usuário excluído com sucesso!"
        )

    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao excluir usuário: {erro}"
        )

    finally:

        if conexao:

            conexao.close()


# ==========================================================
# INICIALIZAR TABELA
# ==========================================================

if __name__ == "__main__":

    criar_tabela_usuarios()

    print(
        "Tabela de usuários inicializada com sucesso!"
    )