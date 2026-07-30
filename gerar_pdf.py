from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from tkinter import filedialog
import os


# ==========================================================
# CONFIGURAÇÕES DA EMPRESA
# ==========================================================

NOME_EMPRESA = "FS ART GESSO & DRYWALL"
RESPONSAVEL = "Frank Correia Souza"
CPF = "029.113.095-02"
TELEFONE = "(79) 99810-7426"

LOGO = "fs_art_gesso.png"


# ==========================================================
# CORES
# ==========================================================

COR_PRINCIPAL = colors.HexColor("#1F4E78")
COR_PRINCIPAL_ESCURO = colors.HexColor("#163A5C")
COR_BORDA = colors.HexColor("#D5DDE5")
COR_TEXTO = colors.HexColor("#222222")
COR_TEXTO_SECUNDARIO = colors.HexColor("#666666")
COR_FUNDO = colors.HexColor("#F7F9FB")
COR_BRANCO = colors.white
COR_VERDE = colors.HexColor("#2E7D32")
COR_AMARELO = colors.HexColor("#F9A825")


# ==========================================================
# LOCALIZAR LOGO
# ==========================================================

def obter_caminho_logo():

    pasta_atual = os.path.dirname(
        os.path.abspath(__file__)
    )

    caminho_logo = os.path.join(
        pasta_atual,
        LOGO
    )

    return caminho_logo


# ==========================================================
# FORMATAR MOEDA
# ==========================================================

def formatar_moeda(valor):

    try:

        if valor is None:
            valor = 0

        valor = float(valor)

    except (ValueError, TypeError):

        valor = 0

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================================
# FORMATAR NÚMERO
# ==========================================================

def formatar_numero(valor):

    try:

        if valor is None:
            valor = 0

        valor = float(valor)

    except (ValueError, TypeError):

        valor = 0

    return (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ==========================================================
# TEXTO SEGURO
# ==========================================================

def texto_seguro(
    valor,
    padrao="Não informado"
):

    if valor is None:

        return padrao

    texto = str(valor).strip()

    if not texto:

        return padrao

    return texto


# ==========================================================
# CONVERTER SQLITE.ROW PARA DICT
# ==========================================================

def converter_orcamento(orcamento):

    try:

        if hasattr(
            orcamento,
            "keys"
        ):

            return {
                chave: orcamento[chave]
                for chave in orcamento.keys()
            }

        return dict(orcamento)

    except Exception:

        return orcamento


# ==========================================================
# DESENHAR LOGO PROPORCIONAL
# ==========================================================

def desenhar_logo_proporcional(
    pdf,
    caminho_logo,
    x,
    y,
    largura_max,
    altura_max
):

    if not os.path.exists(
        caminho_logo
    ):

        print(
            f"Aviso: logo não encontrada: {caminho_logo}"
        )

        return False

    try:

        logo = ImageReader(
            caminho_logo
        )

        largura_original, altura_original = (
            logo.getSize()
        )

        if (
            largura_original <= 0
            or altura_original <= 0
        ):

            return False

        proporcao = min(
            largura_max / largura_original,
            altura_max / altura_original
        )

        largura_final = (
            largura_original
            * proporcao
        )

        altura_final = (
            altura_original
            * proporcao
        )

        x_final = (
            x
            + (
                largura_max
                - largura_final
            ) / 2
        )

        y_final = (
            y
            + (
                altura_max
                - altura_final
            ) / 2
        )

        pdf.drawImage(
            logo,
            x_final,
            y_final,
            width=largura_final,
            height=altura_final,
            preserveAspectRatio=True,
            mask="auto"
        )

        return True

    except Exception as erro:

        print(
            f"Erro ao desenhar logo: {erro}"
        )

        return False


# ==========================================================
# MARCA D'ÁGUA
# ==========================================================

def adicionar_marca_dagua(
    pdf,
    largura_pagina,
    altura_pagina
):

    caminho_logo = obter_caminho_logo()

    if not os.path.exists(
        caminho_logo
    ):

        print(
            f"Aviso: logo não encontrada: {caminho_logo}"
        )

        return

    try:

        logo = ImageReader(
            caminho_logo
        )

        largura_original, altura_original = (
            logo.getSize()
        )

        largura_max = 360
        altura_max = 360

        proporcao = min(
            largura_max / largura_original,
            altura_max / altura_original
        )

        largura_logo = (
            largura_original
            * proporcao
        )

        altura_logo = (
            altura_original
            * proporcao
        )

        x = (
            largura_pagina
            - largura_logo
        ) / 2

        y = (
            altura_pagina
            - altura_logo
        ) / 2

        pdf.saveState()

        try:

            pdf.setFillAlpha(
                0.07
            )

            pdf.setStrokeAlpha(
                0.07
            )

        except Exception:

            pass

        pdf.drawImage(
            logo,
            x,
            y,
            width=largura_logo,
            height=altura_logo,
            preserveAspectRatio=True,
            mask="auto"
        )

        pdf.restoreState()

    except Exception as erro:

        print(
            f"Erro ao adicionar marca d'água: {erro}"
        )


# ==========================================================
# CABEÇALHO
# ==========================================================

def desenhar_cabecalho(
    pdf,
    largura_pagina,
    altura_pagina,
    caminho_logo
):

    altura_cabecalho = 110

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.roundRect(
        30,
        altura_pagina - 125,
        largura_pagina - 60,
        altura_cabecalho,
        10,
        fill=1,
        stroke=0
    )

    if os.path.exists(
        caminho_logo
    ):

        desenhar_logo_proporcional(
            pdf,
            caminho_logo,
            45,
            altura_pagina - 115,
            95,
            85
        )

    pdf.setFillColor(
        COR_BRANCO
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        150,
        altura_pagina - 55,
        NOME_EMPRESA
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawString(
        150,
        altura_pagina - 75,
        f"Responsável: {RESPONSAVEL}"
    )

    pdf.drawString(
        150,
        altura_pagina - 91,
        f"CPF: {CPF}"
    )

    pdf.drawRightString(
        largura_pagina - 50,
        altura_pagina - 75,
        f"Telefone: {TELEFONE}"
    )


# ==========================================================
# TÍTULO DO ORÇAMENTO
# ==========================================================

def desenhar_titulo_orcamento(
    pdf,
    largura_pagina,
    altura_pagina,
    id_orcamento,
    data_criacao
):

    y = altura_pagina - 155

    pdf.setFillColor(
        COR_TEXTO
    )

    pdf.setFont(
        "Helvetica-Bold",
        17
    )

    pdf.drawString(
        40,
        y,
        "ORÇAMENTO"
    )

    texto_numero = (
        f"Nº {id_orcamento}"
    )

    largura_numero = stringWidth(
        texto_numero,
        "Helvetica-Bold",
        12
    )

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.roundRect(
        largura_pagina
        - 55
        - largura_numero
        - 20,
        y - 7,
        largura_numero + 20,
        25,
        5,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        COR_BRANCO
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawCentredString(
        largura_pagina
        - 55
        - (
            largura_numero / 2
        ),
        y + 1,
        texto_numero
    )

    pdf.setFillColor(
        COR_TEXTO_SECUNDARIO
    )

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawRightString(
        largura_pagina - 40,
        y - 20,
        (
            f"Emissão: "
            f"{texto_seguro(data_criacao, 'Não informada')}"
        )
    )

    return y - 45


# ==========================================================
# DADOS DO CLIENTE
# ==========================================================

def desenhar_dados_cliente(
    pdf,
    largura_pagina,
    y,
    cliente_nome,
    cliente_telefone
):

    altura_quadro = 65

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        40,
        y,
        "DADOS DO CLIENTE"
    )

    y -= 12

    pdf.setFillColor(
        COR_FUNDO
    )

    pdf.setStrokeColor(
        COR_BORDA
    )

    pdf.roundRect(
        40,
        y - altura_quadro,
        largura_pagina - 80,
        altura_quadro,
        7,
        fill=1,
        stroke=1
    )

    pdf.setFillColor(
        COR_TEXTO_SECUNDARIO
    )

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    pdf.drawString(
        55,
        y - 20,
        "CLIENTE"
    )

    pdf.setFillColor(
        COR_TEXTO
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        55,
        y - 37,
        texto_seguro(
            cliente_nome
        )
    )

    pdf.setFillColor(
        COR_TEXTO_SECUNDARIO
    )

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    pdf.drawString(
        350,
        y - 20,
        "TELEFONE"
    )

    pdf.setFillColor(
        COR_TEXTO
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        350,
        y - 37,
        texto_seguro(
            cliente_telefone
        )
    )

    return (
        y
        - altura_quadro
        - 25
    )


# ==========================================================
# DETALHES DO SERVIÇO
# ==========================================================

def desenhar_servico(
    pdf,
    largura_pagina,
    y,
    servico,
    area,
    valor_m2,
    valor_total
):

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        40,
        y,
        "DETALHES DO SERVIÇO"
    )

    y -= 15

    largura_tabela = (
        largura_pagina - 80
    )

    altura_cabecalho = 28

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.roundRect(
        40,
        y - altura_cabecalho,
        largura_tabela,
        altura_cabecalho,
        5,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        COR_BRANCO
    )

    pdf.setFont(
        "Helvetica-Bold",
        8
    )

    pdf.drawString(
        52,
        y - 18,
        "SERVIÇO"
    )

    pdf.drawString(
        310,
        y - 18,
        "ÁREA"
    )

    pdf.drawString(
        390,
        y - 18,
        "VALOR M²"
    )

    pdf.drawString(
        485,
        y - 18,
        "TOTAL"
    )

    y -= altura_cabecalho

    pdf.setFillColor(
        colors.white
    )

    pdf.setStrokeColor(
        COR_BORDA
    )

    pdf.roundRect(
        40,
        y - 40,
        largura_tabela,
        40,
        5,
        fill=1,
        stroke=1
    )

    pdf.setFillColor(
        COR_TEXTO
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    texto_servico = str(
        servico
    )

    if len(
        texto_servico
    ) > 42:

        texto_servico = (
            texto_servico[:39]
            + "..."
        )

    pdf.drawString(
        52,
        y - 25,
        texto_servico
    )

    pdf.drawString(
        310,
        y - 25,
        (
            f"{formatar_numero(area)} m²"
        )
    )

    pdf.drawString(
        390,
        y - 25,
        formatar_moeda(
            valor_m2
        )
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        485,
        y - 25,
        formatar_moeda(
            valor_total
        )
    )

    return (
        y
        - 65
    )


# ==========================================================
# VALOR TOTAL
# ==========================================================

def desenhar_valor_total(
    pdf,
    largura_pagina,
    y,
    valor_total
):

    altura = 55

    pdf.setFillColor(
        COR_PRINCIPAL_ESCURO
    )

    pdf.roundRect(
        40,
        y - altura,
        largura_pagina - 80,
        altura,
        8,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        COR_BRANCO
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        58,
        y - 23,
        "VALOR TOTAL DO ORÇAMENTO"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawRightString(
        largura_pagina - 58,
        y - 34,
        formatar_moeda(
            valor_total
        )
    )

    return (
        y
        - altura
        - 22
    )


# ==========================================================
# STATUS
# ==========================================================

def desenhar_status(
    pdf,
    y,
    status
):

    status = texto_seguro(
        status,
        "Pendente"
    )

    status_normalizado = (
        status.lower()
    )

    if status_normalizado in [
        "aprovado",
        "aprovada",
        "concluído",
        "concluida",
        "concluído"
    ]:

        cor_status = COR_VERDE

    else:

        cor_status = COR_AMARELO

    texto_status = (
        f"STATUS: {status.upper()}"
    )

    largura_status = stringWidth(
        texto_status,
        "Helvetica-Bold",
        9
    )

    pdf.setFillColor(
        cor_status
    )

    pdf.roundRect(
        40,
        y - 25,
        largura_status + 22,
        25,
        5,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(
        COR_BRANCO
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        51,
        y - 17,
        texto_status
    )

    return (
        y
        - 45
    )


# ==========================================================
# OBSERVAÇÕES
# ==========================================================

def desenhar_observacoes(
    pdf,
    largura_pagina,
    y
):

    pdf.setFillColor(
        COR_PRINCIPAL
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        40,
        y,
        "OBSERVAÇÕES"
    )

    y -= 12

    pdf.setFillColor(
        COR_FUNDO
    )

    pdf.setStrokeColor(
        COR_BORDA
    )

    pdf.roundRect(
        40,
        y - 48,
        largura_pagina - 80,
        48,
        5,
        fill=1,
        stroke=1
    )

    pdf.setFillColor(
        COR_TEXTO_SECUNDARIO
    )

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.drawString(
        52,
        y - 20,
        "Este orçamento está sujeito a alterações conforme"
    )

    pdf.drawString(
        52,
        y - 33,
        "as condições, medidas e especificações definidas para o serviço."
    )

    return (
        y
        - 70
    )


# ==========================================================
# RODAPÉ
# ==========================================================

def desenhar_rodape(
    pdf,
    largura_pagina
):

    pdf.setStrokeColor(
        COR_BORDA
    )

    pdf.line(
        40,
        55,
        largura_pagina - 40,
        55
    )

    pdf.setFillColor(
        COR_TEXTO_SECUNDARIO
    )

    pdf.setFont(
        "Helvetica",
        7.5
    )

    pdf.drawCentredString(
        largura_pagina / 2,
        40,
        (
            f"{RESPONSAVEL} | "
            f"CPF: {CPF} | "
            f"{TELEFONE}"
        )
    )

    pdf.drawCentredString(
        largura_pagina / 2,
        27,
        (
            f"{NOME_EMPRESA} - "
            f"Orçamento gerado pelo sistema OrçaSmart"
        )
    )


# ==========================================================
# GERAR PDF
# ==========================================================

def gerar_pdf_orcamento(
    orcamento
):

    try:

        if not orcamento:

            return (
                False,
                "Orçamento inválido."
            )

        # Converte sqlite3.Row para dict
        orcamento = converter_orcamento(
            orcamento
        )

        # ==================================================
        # DADOS DO ORÇAMENTO
        # ==================================================

        id_orcamento = orcamento.get(
            "id",
            "000"
        )

        cliente_nome = texto_seguro(
            orcamento.get(
                "cliente_nome"
            )
        )

        cliente_telefone = texto_seguro(
            orcamento.get(
                "cliente_telefone"
            )
        )

        servico = texto_seguro(
            orcamento.get(
                "servico"
            )
        )

        area = orcamento.get(
            "area",
            0
        )

        valor_m2 = orcamento.get(
            "valor_m2",
            0
        )

        valor_total = orcamento.get(
            "valor_total",
            0
        )

        status = texto_seguro(
            orcamento.get(
                "status"
            ),
            "Pendente"
        )

        data_criacao = texto_seguro(
            orcamento.get(
                "data_criacao"
            ),
            "Não informada"
        )

        # ==================================================
        # ESCOLHER LOCAL DO PDF
        # ==================================================

        caminho = filedialog.asksaveasfilename(
            title="Salvar orçamento em PDF",
            defaultextension=".pdf",
            filetypes=[
                (
                    "Arquivo PDF",
                    "*.pdf"
                )
            ],
            initialfile=(
                f"orcamento_{id_orcamento}.pdf"
            )
        )

        if not caminho:

            return (
                False,
                "Operação cancelada."
            )

        # ==================================================
        # CRIAR PDF A4
        # ==================================================

        largura_pagina, altura_pagina = A4

        pdf = canvas.Canvas(
            caminho,
            pagesize=A4
        )

        # ==================================================
        # METADADOS
        # ==================================================

        pdf.setTitle(
            f"Orçamento Nº {id_orcamento}"
        )

        pdf.setAuthor(
            RESPONSAVEL
        )

        pdf.setSubject(
            f"Orçamento - {NOME_EMPRESA}"
        )

        # ==================================================
        # MARCA D'ÁGUA
        # ==================================================

        adicionar_marca_dagua(
            pdf,
            largura_pagina,
            altura_pagina
        )

        # ==================================================
        # CABEÇALHO
        # ==================================================

        caminho_logo = obter_caminho_logo()

        desenhar_cabecalho(
            pdf,
            largura_pagina,
            altura_pagina,
            caminho_logo
        )

        # ==================================================
        # TÍTULO
        # ==================================================

        y = desenhar_titulo_orcamento(
            pdf,
            largura_pagina,
            altura_pagina,
            id_orcamento,
            data_criacao
        )

        # ==================================================
        # CLIENTE
        # ==================================================

        y = desenhar_dados_cliente(
            pdf,
            largura_pagina,
            y,
            cliente_nome,
            cliente_telefone
        )

        # ==================================================
        # SERVIÇO
        # ==================================================

        y = desenhar_servico(
            pdf,
            largura_pagina,
            y,
            servico,
            area,
            valor_m2,
            valor_total
        )

        # ==================================================
        # VALOR TOTAL
        # ==================================================

        y = desenhar_valor_total(
            pdf,
            largura_pagina,
            y,
            valor_total
        )

        # ==================================================
        # STATUS
        # ==================================================

        y = desenhar_status(
            pdf,
            y,
            status
        )

        # ==================================================
        # OBSERVAÇÕES
        # ==================================================

        desenhar_observacoes(
            pdf,
            largura_pagina,
            y
        )

        # ==================================================
        # RODAPÉ
        # ==================================================

        desenhar_rodape(
            pdf,
            largura_pagina
        )

        # ==================================================
        # FINALIZAR
        # ==================================================

        pdf.showPage()

        pdf.save()

        return (
            True,
            caminho
        )

    except Exception as erro:

        print(
            f"Erro ao gerar PDF: {erro}"
        )

        return (
            False,
            str(erro)
        )