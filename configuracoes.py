import sqlite3

from banco import conectar


# ==========================================================
# BUSCAR CONFIGURAÇÕES DA EMPRESA
# ==========================================================

def buscar_configuracoes(usuario_id):

    if not usuario_id:
        return None

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                usuario_id,
                nome_empresa,
                responsavel,
                cpf_cnpj,
                telefone,
                email,
                endereco,
                logo

            FROM configuracoes_empresa

            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))

        return cursor.fetchone()

    except sqlite3.Error as erro:

        print(
            f"Erro ao buscar configurações: {erro}"
        )

        return None

    finally:

        conexao.close()


# ==========================================================
# SALVAR CONFIGURAÇÕES DA EMPRESA
# ==========================================================

def salvar_configuracoes(
    usuario_id,
    nome_empresa,
    responsavel,
    cpf_cnpj,
    telefone,
    email,
    endereco,
    logo=""
):

    if not usuario_id:

        return (
            False,
            "Usuário inválido."
        )

    nome_empresa = (
        nome_empresa.strip()
        if nome_empresa
        else ""
    )

    responsavel = (
        responsavel.strip()
        if responsavel
        else ""
    )

    cpf_cnpj = (
        cpf_cnpj.strip()
        if cpf_cnpj
        else ""
    )

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

    logo = (
        logo.strip()
        if logo
        else ""
    )

    if not nome_empresa:

        return (
            False,
            "O nome da empresa é obrigatório."
        )

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # ==================================================
        # VERIFICAR SE JÁ EXISTE CONFIGURAÇÃO
        # ==================================================

        cursor.execute("""
            SELECT id
            FROM configuracoes_empresa
            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))

        configuracao = cursor.fetchone()

        # ==================================================
        # ATUALIZAR
        # ==================================================

        if configuracao:

            cursor.execute("""
                UPDATE configuracoes_empresa

                SET
                    nome_empresa = ?,
                    responsavel = ?,
                    cpf_cnpj = ?,
                    telefone = ?,
                    email = ?,
                    endereco = ?,
                    logo = ?

                WHERE usuario_id = ?
            """, (

                nome_empresa,

                responsavel,

                cpf_cnpj,

                telefone,

                email,

                endereco,

                logo,

                usuario_id

            ))

            conexao.commit()

            return (
                True,
                "Configurações atualizadas com sucesso!"
            )

        # ==================================================
        # CADASTRAR
        # ==================================================

        cursor.execute("""
            INSERT INTO configuracoes_empresa (

                usuario_id,

                nome_empresa,

                responsavel,

                cpf_cnpj,

                telefone,

                email,

                endereco,

                logo

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            usuario_id,

            nome_empresa,

            responsavel,

            cpf_cnpj,

            telefone,

            email,

            endereco,

            logo

        ))

        conexao.commit()

        return (
            True,
            "Configurações salvas com sucesso!"
        )

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao salvar configurações: {erro}"
        )

        return (
            False,
            "Não foi possível salvar as configurações."
        )

    finally:

        conexao.close()


# ==========================================================
# EXCLUIR CONFIGURAÇÕES
# ==========================================================

def excluir_configuracoes(usuario_id):

    if not usuario_id:

        return (
            False,
            "Usuário inválido."
        )

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM configuracoes_empresa

            WHERE usuario_id = ?

        """, (
            usuario_id,
        ))

        if cursor.rowcount == 0:

            return (
                False,
                "Nenhuma configuração encontrada."
            )

        conexao.commit()

        return (
            True,
            "Configurações excluídas com sucesso!"
        )

    except sqlite3.Error as erro:

        conexao.rollback()

        print(
            f"Erro ao excluir configurações: {erro}"
        )

        return (
            False,
            "Não foi possível excluir as configurações."
        )

    finally:

        conexao.close()


# ==========================================================
# TESTE DIRETO
# ==========================================================

if __name__ == "__main__":

    print(
        "Módulo de configurações carregado com sucesso!"
    )