
import sqlite3


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

BANCO_DADOS = "orcamentos.db"


# ==========================================================
# CONEXÃO COM BANCO
# ==========================================================

def conectar_banco():

    conexao = sqlite3.connect(
        BANCO_DADOS
    )

    # Permite acessar as colunas pelo nome:
    # orcamento["id"]
    # orcamento["cliente_nome"]
    # orcamento["servico"]

    conexao.row_factory = sqlite3.Row

    return conexao


# ==========================================================
# LISTAR ORÇAMENTOS
# ==========================================================

def listar_orcamentos():

    conexao = conectar_banco()

    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT
                orcamentos.id AS id,
                orcamentos.cliente_id AS cliente_id,

                clientes.nome AS cliente_nome,
                clientes.telefone AS cliente_telefone,

                orcamentos.servico AS servico,
                orcamentos.area AS area,
                orcamentos.valor_m2 AS valor_m2,
                orcamentos.valor_total AS valor_total,
                orcamentos.status AS status,
                orcamentos.data_criacao AS data_criacao

            FROM orcamentos

            INNER JOIN clientes
                ON orcamentos.cliente_id = clientes.id

            ORDER BY orcamentos.id DESC
        """)

        orcamentos = cursor.fetchall()

        return orcamentos

    except sqlite3.Error as erro:

        print(
            f"Erro ao listar orçamentos: {erro}"
        )

        return []

    finally:

        conexao.close()


# ==========================================================
# TESTE DO ARQUIVO
# ==========================================================

if __name__ == "__main__":

    orcamentos = listar_orcamentos()

    print(
        "\n======= ORÇAMENTOS ========\n"
    )

    if orcamentos:

        for orcamento in orcamentos:

            print(
                f"Orçamento: "
                f"{orcamento['id']}"
            )

            print(
                f"Cliente: "
                f"{orcamento['cliente_nome']}"
            )

            print(
                f"Telefone: "
                f"{orcamento['cliente_telefone'] or 'Não informado'}"
            )

            print(
                f"Serviço: "
                f"{orcamento['servico']}"
            )

            print(
                f"Área: "
                f"{float(orcamento['area']):.2f} m²"
            )

            print(
                f"Valor por m²: "
                f"R$ {float(orcamento['valor_m2']):.2f}"
            )

            print(
                f"Valor total: "
                f"R$ {float(orcamento['valor_total']):.2f}"
            )

            print(
                f"Status: "
                f"{orcamento['status']}"
            )

            print(
                f"Data: "
                f"{orcamento['data_criacao']}"
            )

            print(
                "-" * 40
            )

    else:

        print(
            "Nenhum orçamento cadastrado."
        )

