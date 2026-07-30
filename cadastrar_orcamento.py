
import sqlite3

from banco import conectar


# ==========================================================
# VALIDAÇÃO DOS DADOS
# ==========================================================

def validar_orcamento(servico, area, valor_m2):
    """
    Valida os dados antes de salvar um orçamento.
    """

    # Validação do serviço
    if not servico or not servico.strip():
        return False, "O serviço é obrigatório."

    # Validação da área
    try:
        area = float(area)
    except (ValueError, TypeError):
        return False, "A área deve ser um valor numérico."

    if area <= 0:
        return False, "A área deve ser maior que zero."

    # Validação do valor por m²
    try:
        valor_m2 = float(valor_m2)
    except (ValueError, TypeError):
        return False, "O valor do m² deve ser numérico."

    if valor_m2 <= 0:
        return False, "O valor do m² deve ser maior que zero."

    return True, ""


# ==========================================================
# CADASTRAR ORÇAMENTO
# ==========================================================

def cadastrar_orcamento(
    cliente_id,
    servico,
    area,
    valor_m2,
    status="Pendente"
):
    """
    Cadastra um novo orçamento.

    O valor total é calculado automaticamente:

    área × valor do m²
    """

    # Verifica cliente
    if not cliente_id:
        return False, "Selecione um cliente."

    # Valida dados
    valido, mensagem = validar_orcamento(
        servico,
        area,
        valor_m2
    )

    if not valido:
        return False, mensagem

    # Conversão dos valores
    area = float(area)
    valor_m2 = float(valor_m2)

    # Limpa o serviço
    servico = servico.strip()

    # Calcula o valor total
    valor_total = area * valor_m2

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # Verifica se o cliente existe
        cursor.execute("""
            SELECT id
            FROM clientes
            WHERE id = ?
        """, (cliente_id,))

        cliente = cursor.fetchone()

        if cliente is None:
            return False, "Cliente não encontrado."

        # Insere orçamento
        cursor.execute("""
            INSERT INTO orcamentos (
                cliente_id,
                servico,
                area,
                valor_m2,
                valor_total,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cliente_id,
            servico,
            area,
            valor_m2,
            valor_total,
            status
        ))

        conexao.commit()

        return True, "Orçamento cadastrado com sucesso!"

    except sqlite3.Error as erro:

        conexao.rollback()

        print(f"Erro ao cadastrar orçamento: {erro}")

        return False, "Não foi possível cadastrar o orçamento."

    finally:

        conexao.close()


# ==========================================================
# LISTAR ORÇAMENTOS
# ==========================================================

def listar_orcamentos():
    """
    Lista todos os orçamentos com os dados do cliente.
    """

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                o.id,
                o.cliente_id,
                c.nome AS cliente_nome,
                c.telefone AS cliente_telefone,
                o.servico,
                o.area,
                o.valor_m2,
                o.valor_total,
                o.status,
                o.data_criacao

            FROM orcamentos o

            INNER JOIN clientes c
                ON c.id = o.cliente_id

            ORDER BY o.id DESC
        """)

        return cursor.fetchall()

    except sqlite3.Error as erro:

        print(f"Erro ao listar orçamentos: {erro}")

        return []

    finally:

        conexao.close()


# ==========================================================
# PESQUISAR ORÇAMENTOS
# ==========================================================

def pesquisar_orcamentos(termo):
    """
    Pesquisa orçamentos por:

    - Nome do cliente
    - Telefone
    - Serviço
    """

    termo = termo.strip() if termo else ""

    if not termo:
        return listar_orcamentos()

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                o.id,
                o.cliente_id,
                c.nome AS cliente_nome,
                c.telefone AS cliente_telefone,
                o.servico,
                o.area,
                o.valor_m2,
                o.valor_total,
                o.status,
                o.data_criacao

            FROM orcamentos o

            INNER JOIN clientes c
                ON c.id = o.cliente_id

            WHERE c.nome LIKE ?
               OR c.telefone LIKE ?
               OR o.servico LIKE ?

            ORDER BY o.id DESC
        """, (
            f"%{termo}%",
            f"%{termo}%",
            f"%{termo}%"
        ))

        return cursor.fetchall()

    except sqlite3.Error as erro:

        print(f"Erro ao pesquisar orçamentos: {erro}")

        return []

    finally:

        conexao.close()


# ==========================================================
# BUSCAR ORÇAMENTO POR ID
# ==========================================================

def buscar_orcamento(orcamento_id):
    """
    Busca um orçamento específico pelo ID.
    """

    if not orcamento_id:
        return None

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                o.id,
                o.cliente_id,
                c.nome AS cliente_nome,
                c.telefone AS cliente_telefone,
                o.servico,
                o.area,
                o.valor_m2,
                o.valor_total,
                o.status,
                o.data_criacao

            FROM orcamentos o

            INNER JOIN clientes c
                ON c.id = o.cliente_id

            WHERE o.id = ?
        """, (orcamento_id,))

        return cursor.fetchone()

    except sqlite3.Error as erro:

        print(f"Erro ao buscar orçamento: {erro}")

        return None

    finally:

        conexao.close()


# ==========================================================
# EDITAR ORÇAMENTO
# ==========================================================

def editar_orcamento(
    orcamento_id,
    cliente_id,
    servico,
    area,
    valor_m2,
    status="Pendente"
):
    """
    Edita um orçamento existente.

    O valor total é recalculado automaticamente.
    """

    if not orcamento_id:
        return False, "ID do orçamento inválido."

    if not cliente_id:
        return False, "Selecione um cliente."

    # Validação
    valido, mensagem = validar_orcamento(
        servico,
        area,
        valor_m2
    )

    if not valido:
        return False, mensagem

    area = float(area)
    valor_m2 = float(valor_m2)

    valor_total = area * valor_m2

    servico = servico.strip()

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        # Verifica cliente
        cursor.execute("""
            SELECT id
            FROM clientes
            WHERE id = ?
        """, (cliente_id,))

        if cursor.fetchone() is None:
            return False, "Cliente não encontrado."

        # Atualiza orçamento
        cursor.execute("""
            UPDATE orcamentos
            SET
                cliente_id = ?,
                servico = ?,
                area = ?,
                valor_m2 = ?,
                valor_total = ?,
                status = ?

            WHERE id = ?
        """, (
            cliente_id,
            servico,
            area,
            valor_m2,
            valor_total,
            status,
            orcamento_id
        ))

        if cursor.rowcount == 0:
            return False, "Orçamento não encontrado."

        conexao.commit()

        return True, "Orçamento atualizado com sucesso!"

    except sqlite3.Error as erro:

        conexao.rollback()

        print(f"Erro ao editar orçamento: {erro}")

        return False, "Não foi possível atualizar o orçamento."

    finally:

        conexao.close()


# ==========================================================
# EXCLUIR ORÇAMENTO
# ==========================================================

def excluir_orcamento(orcamento_id):
    """
    Exclui um orçamento pelo ID.
    """

    if not orcamento_id:
        return False, "ID do orçamento inválido."

    conexao = conectar()

    try:

        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM orcamentos
            WHERE id = ?
        """, (orcamento_id,))

        if cursor.rowcount == 0:
            return False, "Orçamento não encontrado."

        conexao.commit()

        return True, "Orçamento excluído com sucesso!"

    except sqlite3.Error as erro:

        conexao.rollback()

        print(f"Erro ao excluir orçamento: {erro}")

        return False, "Não foi possível excluir o orçamento."

    finally:

        conexao.close()

