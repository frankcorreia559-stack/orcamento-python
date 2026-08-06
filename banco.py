import sqlite3


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

BANCO = "orcamentos.db"


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

def conectar():

    conexao = sqlite3.connect(BANCO)

    conexao.row_factory = sqlite3.Row

    return conexao


# ==========================================================
# CRIAR TABELAS
# ==========================================================

def criar_tabelas():

    conexao = conectar()

    cursor = conexao.cursor()

    # ------------------------------------------------------
    # TABELA CLIENTES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL,

            nome TEXT NOT NULL,

            telefone TEXT,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id)

        )
    """)

    # ------------------------------------------------------
    # TABELA ORÇAMENTOS
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orcamentos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL,

            cliente TEXT NOT NULL,

            servico TEXT NOT NULL,

            area REAL NOT NULL,

            valor_m2 REAL NOT NULL,

            valor_total REAL NOT NULL,

            status TEXT DEFAULT 'Pendente',

            data_criacao TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (usuario_id)
            REFERENCES usuarios(id)

        )
    """)

    conexao.commit()

    conexao.close()


# ==========================================================
# MIGRAR BANCO
# ==========================================================

def migrar_banco():

    conexao = conectar()

    cursor = conexao.cursor()

    try:

        # --------------------------------------------------
        # VERIFICAR TABELA CLIENTES
        # --------------------------------------------------

        cursor.execute("""
            PRAGMA table_info(clientes)
        """)

        colunas_clientes = cursor.fetchall()

        nomes_clientes = [
            coluna["name"]
            for coluna in colunas_clientes
        ]

        # --------------------------------------------------
        # ADICIONAR USUARIO_ID EM CLIENTES
        # --------------------------------------------------

        if "usuario_id" not in nomes_clientes:

            cursor.execute("""
                ALTER TABLE clientes

                ADD COLUMN usuario_id INTEGER
            """)


        # --------------------------------------------------
        # VERIFICAR TABELA ORÇAMENTOS
        # --------------------------------------------------

        cursor.execute("""
            PRAGMA table_info(orcamentos)
        """)

        colunas_orcamentos = cursor.fetchall()

        nomes_orcamentos = [
            coluna["name"]
            for coluna in colunas_orcamentos
        ]

        # --------------------------------------------------
        # CORRIGIR CLIENTE
        # --------------------------------------------------

        if (
            "client" in nomes_orcamentos
            and "cliente" not in nomes_orcamentos
        ):

            cursor.execute("""
                ALTER TABLE orcamentos

                RENAME COLUMN client TO cliente
            """)


        # --------------------------------------------------
        # CORRIGIR CLIENTE_NOME
        # --------------------------------------------------

        if (
            "cliente_nome" in nomes_orcamentos
            and "cliente" not in nomes_orcamentos
        ):

            cursor.execute("""
                ALTER TABLE orcamentos

                RENAME COLUMN cliente_nome TO cliente
            """)


        # --------------------------------------------------
        # CORRIGIR VALOR_M²
        # --------------------------------------------------

        if (
            "valor_m²" in nomes_orcamentos
            and "valor_m2" not in nomes_orcamentos
        ):

            cursor.execute("""
                ALTER TABLE orcamentos

                RENAME COLUMN "valor_m²"
                TO valor_m2
            """)


        # --------------------------------------------------
        # ADICIONAR USUARIO_ID
        # --------------------------------------------------

        if "usuario_id" not in nomes_orcamentos:

            cursor.execute("""
                ALTER TABLE orcamentos

                ADD COLUMN usuario_id INTEGER
            """)


        # --------------------------------------------------
        # ADICIONAR STATUS
        # --------------------------------------------------

        if "status" not in nomes_orcamentos:

            cursor.execute("""
                ALTER TABLE orcamentos

                ADD COLUMN status TEXT
                DEFAULT 'Pendente'
            """)


        # --------------------------------------------------
        # ADICIONAR DATA
        # --------------------------------------------------

        if "data_criacao" not in nomes_orcamentos:

            cursor.execute("""
                ALTER TABLE orcamentos

                ADD COLUMN data_criacao TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
            """)


        conexao.commit()


    except sqlite3.Error as erro:

        print(
            f"Erro na migração do banco: {erro}"
        )


    finally:

        conexao.close()


# ==========================================================
# CADASTRAR CLIENTE
# ==========================================================

def cadastrar_cliente(
    usuario_id,
    nome,
    telefone=""
):

    if not nome or not nome.strip():

        return (
            False,
            "O nome do cliente é obrigatório."
        )


    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            INSERT INTO clientes
            (
                usuario_id,
                nome,
                telefone
            )

            VALUES (?, ?, ?)
        """, (
            usuario_id,
            nome.strip(),
            telefone.strip()
        ))


        conexao.commit()

        conexao.close()


        return (
            True,
            "Cliente cadastrado com sucesso!"
        )


    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao cadastrar cliente: {erro}"
        )


# ==========================================================
# LISTAR CLIENTES
# ==========================================================

def listar_clientes(
    usuario_id
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            SELECT
                id,
                nome,
                telefone

            FROM clientes

            WHERE usuario_id = ?

            ORDER BY id DESC
        """, (
            usuario_id,
        ))


        clientes = cursor.fetchall()

        conexao.close()


        return clientes


    except sqlite3.Error as erro:

        print(
            f"Erro ao listar clientes: {erro}"
        )

        return []


# ==========================================================
# BUSCAR CLIENTES
# ==========================================================

def buscar_clientes(
    usuario_id,
    nome
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            SELECT
                id,
                nome,
                telefone

            FROM clientes

            WHERE usuario_id = ?

            AND nome LIKE ?

            ORDER BY nome
        """, (
            usuario_id,
            f"%{nome}%"
        ))


        clientes = cursor.fetchall()

        conexao.close()


        return clientes


    except sqlite3.Error as erro:

        print(
            f"Erro ao buscar clientes: {erro}"
        )

        return []


# ==========================================================
# EDITAR CLIENTE
# ==========================================================

def editar_cliente(
    usuario_id,
    id_cliente,
    nome,
    telefone=""
):

    if not nome or not nome.strip():

        return (
            False,
            "O nome do cliente é obrigatório."
        )


    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            UPDATE clientes

            SET
                nome = ?,
                telefone = ?

            WHERE id = ?

            AND usuario_id = ?
        """, (
            nome.strip(),
            telefone.strip(),
            id_cliente,
            usuario_id
        ))


        conexao.commit()


        if cursor.rowcount == 0:

            conexao.close()

            return (
                False,
                "Cliente não encontrado."
            )


        conexao.close()


        return (
            True,
            "Cliente atualizado com sucesso!"
        )


    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao editar cliente: {erro}"
        )


# ==========================================================
# EXCLUIR CLIENTE
# ==========================================================

def excluir_cliente(
    usuario_id,
    id_cliente
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            DELETE FROM clientes

            WHERE id = ?

            AND usuario_id = ?
        """, (
            id_cliente,
            usuario_id
        ))


        conexao.commit()


        if cursor.rowcount == 0:

            conexao.close()

            return (
                False,
                "Cliente não encontrado."
            )


        conexao.close()


        return (
            True,
            "Cliente excluído com sucesso!"
        )


    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao excluir cliente: {erro}"
        )


# ==========================================================
# CADASTRAR ORÇAMENTO
# ==========================================================

def cadastrar_orcamento(
    usuario_id,
    cliente,
    servico,
    area,
    valor_m2
):

    if not cliente or not cliente.strip():

        return (
            False,
            "O cliente é obrigatório."
        )


    if not servico or not servico.strip():

        return (
            False,
            "O serviço é obrigatório."
        )


    try:

        area = float(area)

        valor_m2 = float(valor_m2)


    except (
        ValueError,
        TypeError
    ):

        return (
            False,
            "Área e valor por m² devem ser numéricos."
        )


    if area <= 0:

        return (
            False,
            "A área deve ser maior que zero."
        )


    if valor_m2 <= 0:

        return (
            False,
            "O valor por m² deve ser maior que zero."
        )


    valor_total = (
        area
        * valor_m2
    )


    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            INSERT INTO orcamentos
            (
                usuario_id,
                cliente,
                servico,
                area,
                valor_m2,
                valor_total,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario_id,
            cliente.strip(),
            servico.strip(),
            area,
            valor_m2,
            valor_total,
            "Pendente"
        ))


        conexao.commit()

        conexao.close()


        return (
            True,
            "Orçamento cadastrado com sucesso!"
        )


    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao cadastrar orçamento: {erro}"
        )


# ==========================================================
# LISTAR ORÇAMENTOS
# ==========================================================

def listar_orcamentos(
    usuario_id
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            SELECT
                id,
                cliente,
                servico,
                area,
                valor_m2,
                valor_total,
                status,
                data_criacao

            FROM orcamentos

            WHERE usuario_id = ?

            ORDER BY id DESC
        """, (
            usuario_id,
        ))


        orcamentos = cursor.fetchall()

        conexao.close()


        return orcamentos


    except sqlite3.Error as erro:

        print(
            f"Erro ao listar orçamentos: {erro}"
        )

        return []


# ==========================================================
# BUSCAR ORÇAMENTOS
# ==========================================================

def buscar_orcamentos(
    usuario_id,
    cliente
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            SELECT
                id,
                cliente,
                servico,
                area,
                valor_m2,
                valor_total,
                status,
                data_criacao

            FROM orcamentos

            WHERE usuario_id = ?

            AND cliente LIKE ?

            ORDER BY id DESC
        """, (
            usuario_id,
            f"%{cliente}%"
        ))


        orcamentos = cursor.fetchall()

        conexao.close()


        return orcamentos


    except sqlite3.Error as erro:

        print(
            f"Erro ao buscar orçamentos: {erro}"
        )

        return []


# ==========================================================
# EXCLUIR ORÇAMENTO
# ==========================================================

def excluir_orcamento(
    usuario_id,
    id_orcamento
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        cursor.execute("""
            DELETE FROM orcamentos

            WHERE id = ?

            AND usuario_id = ?
        """, (
            id_orcamento,
            usuario_id
        ))


        conexao.commit()


        if cursor.rowcount == 0:

            conexao.close()

            return (
                False,
                "Orçamento não encontrado."
            )


        conexao.close()


        return (
            True,
            "Orçamento excluído com sucesso!"
        )


    except sqlite3.Error as erro:

        return (
            False,
            f"Erro ao excluir orçamento: {erro}"
        )


# ==========================================================
# ESTATÍSTICAS
# ==========================================================

def obter_estatisticas(
    usuario_id
):

    try:

        conexao = conectar()

        cursor = conexao.cursor()


        # --------------------------------------------------
        # CLIENTES DO USUÁRIO
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM clientes

            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))


        clientes = (
            cursor.fetchone()["total"]
        )


        # --------------------------------------------------
        # ORÇAMENTOS DO USUÁRIO
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM orcamentos

            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))


        orcamentos = (
            cursor.fetchone()["total"]
        )


        # --------------------------------------------------
        # VALOR TOTAL DO USUÁRIO
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(valor_total),
                    0
                ) AS total

            FROM orcamentos

            WHERE usuario_id = ?
        """, (
            usuario_id,
        ))


        valor_total = (
            cursor.fetchone()["total"]
        )


        conexao.close()


        return {

            "clientes":
                clientes,

            "orcamentos":
                orcamentos,

            "valor_total":
                float(
                    valor_total or 0
                )

        }


    except sqlite3.Error as erro:

        print(
            f"Erro ao obter estatísticas: {erro}"
        )


        return {

            "clientes": 0,

            "orcamentos": 0,

            "valor_total": 0

        }


# ==========================================================
# INICIALIZAR BANCO
# ==========================================================

if __name__ == "__main__":

    criar_tabelas()

    migrar_banco()

    print(
        "Banco de dados inicializado com sucesso!"
    )