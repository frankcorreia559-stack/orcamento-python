import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

from banco import inicializar_banco

from gerar_pdf import gerar_pdf_orcamento

from clientes import (
    cadastrar_cliente,
    listar_clientes,
    pesquisar_clientes,
    editar_cliente,
    excluir_cliente
)

from cadastrar_orcamento import (
    cadastrar_orcamento,
    listar_orcamentos,
    pesquisar_orcamentos,
    buscar_orcamento,
    editar_orcamento,
    excluir_orcamento
)

# ==========================================================
# MATPLOTLIB
# ==========================================================

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==========================================================
# CORES DO ORÇASMART
# ==========================================================

COR_PRINCIPAL = "#1F4E78"
COR_SECUNDARIA = "#2E75B6"
COR_FUNDO = "#F5F7FA"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#222222"
COR_TEXTO_SECUNDARIO = "#666666"
COR_BORDA = "#E1E5EA"


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def formatar_moeda(valor):

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        valor = 0

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_numero(valor):

    try:
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
# CLASSE PRINCIPAL
# ==========================================================

class Sistema(ctk.CTk):

    def __init__(self):

        super().__init__()

        # --------------------------------------------------
        # CONFIGURAÇÃO DA JANELA
        # --------------------------------------------------

        self.title(
            "OrçaSmart - FS ART Gesso & Drywall"
        )

        self.geometry(
            "1280x750"
        )

        self.minsize(
            1050,
            650
        )

        self.configure(
            fg_color=COR_FUNDO
        )

        # --------------------------------------------------
        # BANCO DE DADOS
        # --------------------------------------------------

        inicializar_banco()

        # --------------------------------------------------
        # INTERFACE
        # --------------------------------------------------

        self.criar_menu_lateral()

        self.criar_area_principal()

        # --------------------------------------------------
        # DASHBOARD INICIAL
        # --------------------------------------------------

        self.abrir_dashboard()

    # ======================================================
    # MENU LATERAL
    # ======================================================

    def criar_menu_lateral(self):

        self.menu = ctk.CTkFrame(

            self,

            width=230,

            corner_radius=0,

            fg_color=COR_PRINCIPAL

        )

        self.menu.pack(

            side="left",

            fill="y"

        )

        self.menu.pack_propagate(
            False
        )

        # --------------------------------------------------
        # LOGO / NOME
        # --------------------------------------------------

        self.logo_nome = ctk.CTkLabel(

            self.menu,

            text=(
                "FS ART\n"
                "Gesso & Drywall"
            ),

            font=(
                "Arial",
                21,
                "bold"
            ),

            text_color="white",

            justify="center"

        )

        self.logo_nome.pack(

            pady=(
                35,
                40
            )

        )

        # --------------------------------------------------
        # MENU
        # --------------------------------------------------

        botoes = [

            (
                "🏠  Dashboard",
                self.abrir_dashboard
            ),

            (
                "👤  Clientes",
                self.abrir_clientes
            ),

            (
                "📋  Orçamentos",
                self.abrir_orcamentos
            ),

            (
                "📄  Relatórios",
                self.abrir_relatorios
            ),

            (
                "⚙  Configurações",
                self.abrir_configuracoes
            )

        ]

        self.botoes_menu = []

        for texto, comando in botoes:

            botao = ctk.CTkButton(

                self.menu,

                text=texto,

                width=190,

                height=45,

                corner_radius=8,

                font=(
                    "Arial",
                    14,
                    "bold"
                ),

                fg_color="transparent",

                hover_color=COR_SECUNDARIA,

                text_color="white",

                anchor="w",

                command=comando

            )

            botao.pack(

                pady=6,

                padx=18

            )

            self.botoes_menu.append(
                botao
            )

        # --------------------------------------------------
        # RODAPÉ DO MENU
        # --------------------------------------------------

        ctk.CTkLabel(

            self.menu,

            text=(
                "OrçaSmart\n"
                "Sistema de Orçamentos"
            ),

            font=(
                "Arial",
                10
            ),

            text_color="#DCE6F0"

        ).pack(

            side="bottom",

            pady=25

        )

    # ======================================================
    # ÁREA PRINCIPAL
    # ======================================================

    def criar_area_principal(self):

        self.conteudo = ctk.CTkFrame(

            self,

            corner_radius=0,

            fg_color=COR_FUNDO

        )

        self.conteudo.pack(

            side="right",

            fill="both",

            expand=True

        )

        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        self.cabecalho = ctk.CTkFrame(

            self.conteudo,

            height=80,

            corner_radius=0,

            fg_color=COR_CARD

        )

        self.cabecalho.pack(

            fill="x"

        )

        self.cabecalho.pack_propagate(
            False
        )

        self.titulo = ctk.CTkLabel(

            self.cabecalho,

            text="Dashboard",

            font=(
                "Arial",
                26,
                "bold"
            ),

            text_color=COR_TEXTO

        )

        self.titulo.pack(

            side="left",

            padx=30

        )

        # --------------------------------------------------
        # BOTÃO ATUALIZAR
        # --------------------------------------------------

        self.botao_atualizar = ctk.CTkButton(

            self.cabecalho,

            text="🔄 Atualizar",

            width=120,

            height=36,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=self.atualizar_dashboard

        )

        self.botao_atualizar.pack(

            side="right",

            padx=25

        )

        # --------------------------------------------------
        # ÁREA DAS PÁGINAS
        # --------------------------------------------------

        self.pagina = ctk.CTkScrollableFrame(

            self.conteudo,

            corner_radius=0,

            fg_color=COR_FUNDO

        )

        self.pagina.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

    # ======================================================
    # LIMPAR PÁGINA
    # ======================================================

    def limpar_pagina(self):

        for widget in self.pagina.winfo_children():

            widget.destroy()

    # ======================================================
    # DASHBOARD
    # ======================================================

    def abrir_dashboard(self):

        self.limpar_pagina()

        self.titulo.configure(

            text="Dashboard"

        )

        # --------------------------------------------------
        # BUSCAR DADOS
        # --------------------------------------------------

        clientes = listar_clientes()

        orcamentos = listar_orcamentos()

        total_clientes = len(
            clientes
        )

        total_orcamentos = len(
            orcamentos
        )

        # --------------------------------------------------
        # CONTADORES
        # --------------------------------------------------

        aprovados = 0

        pendentes = 0

        recusados = 0

        concluidos = 0

        valor_total = 0

        for orcamento in orcamentos:

            try:

                valor_total += float(

                    orcamento["valor_total"]

                    or 0

                )

            except (
                ValueError,
                TypeError,
                KeyError
            ):

                pass

            status = (

                str(

                    orcamento["status"]

                    or "Pendente"

                )

                .strip()

                .lower()

            )

            if status == "aprovado":

                aprovados += 1

            elif status == "pendente":

                pendentes += 1

            elif status == "recusado":

                recusados += 1

            elif status == "concluído" or status == "concluido":

                concluidos += 1

        # --------------------------------------------------
        # TAXA DE APROVAÇÃO
        # --------------------------------------------------

        if total_orcamentos > 0:

            taxa_aprovacao = (

                aprovados /

                total_orcamentos

            ) * 100

        else:

            taxa_aprovacao = 0

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        titulo_dashboard = ctk.CTkLabel(

            self.pagina,

            text=(
                "Visão geral do OrçaSmart"
            ),

            font=(
                "Arial",
                22,
                "bold"
            ),

            text_color=COR_TEXTO

        )

        titulo_dashboard.pack(

            anchor="w",

            padx=20,

            pady=(
                10,
                20
            )

        )

        # --------------------------------------------------
        # CARDS
        # --------------------------------------------------

        cards = ctk.CTkFrame(

            self.pagina,

            fg_color="transparent"

        )

        cards.pack(

            fill="x",

            padx=10,

            pady=5

        )

        for coluna in range(4):

            cards.grid_columnconfigure(

                coluna,

                weight=1

            )

        # --------------------------------------------------
        # CARD 1
        # --------------------------------------------------

        self.criar_card_dashboard(

            cards,

            "👤",

            "Clientes",

            str(total_clientes)

        ).grid(

            row=0,

            column=0,

            padx=8,

            pady=8,

            sticky="nsew"

        )

        # --------------------------------------------------
        # CARD 2
        # --------------------------------------------------

        self.criar_card_dashboard(

            cards,

            "📋",

            "Orçamentos",

            str(total_orcamentos)

        ).grid(

            row=0,

            column=1,

            padx=8,

            pady=8,

            sticky="nsew"

        )

        # --------------------------------------------------
        # CARD 3
        # --------------------------------------------------

        self.criar_card_dashboard(

            cards,

            "✅",

            "Aprovados",

            str(aprovados)

        ).grid(

            row=0,

            column=2,

            padx=8,

            pady=8,

            sticky="nsew"

        )

        # --------------------------------------------------
        # CARD 4
        # --------------------------------------------------

        self.criar_card_dashboard(

            cards,

            "💰",

            "Valor Total",

            formatar_moeda(

                valor_total

            )

        ).grid(

            row=0,

            column=3,

            padx=8,

            pady=8,

            sticky="nsew"

        )

        # --------------------------------------------------
        # ÁREA DOS GRÁFICOS
        # --------------------------------------------------

        graficos = ctk.CTkFrame(

            self.pagina,

            fg_color="transparent"

        )

        graficos.pack(

            fill="x",

            expand=False,

            padx=10,

            pady=15

        )

        graficos.grid_columnconfigure(

            0,

            weight=1

        )

        graficos.grid_columnconfigure(

            1,

            weight=1

        )

        # --------------------------------------------------
        # GRÁFICO DE STATUS
        # --------------------------------------------------

        frame_status = ctk.CTkFrame(

            graficos,

            corner_radius=15,

            fg_color=COR_CARD

        )

        frame_status.grid(

            row=0,

            column=0,

            padx=8,

            sticky="nsew"

        )

        ctk.CTkLabel(

            frame_status,

            text="Distribuição dos Orçamentos",

            font=(

                "Arial",

                17,

                "bold"

            ),

            text_color=COR_TEXTO

        ).pack(

            pady=10

        )

        self.criar_grafico_status(

            frame_status,

            pendentes,

            aprovados,

            recusados,

            concluidos

        )

        # --------------------------------------------------
        # GRÁFICO FINANCEIRO
        # --------------------------------------------------

        frame_valores = ctk.CTkFrame(

            graficos,

            corner_radius=15,

            fg_color=COR_CARD

        )

        frame_valores.grid(

            row=0,

            column=1,

            padx=8,

            sticky="nsew"

        )

        ctk.CTkLabel(

            frame_valores,

            text="Valor por Status",

            font=(

                "Arial",

                17,

                "bold"

            ),

            text_color=COR_TEXTO

        ).pack(

            pady=10

        )

        self.criar_grafico_valores(

            frame_valores,

            orcamentos

        )

        # --------------------------------------------------
        # ÁREA INFERIOR
        # --------------------------------------------------

        inferior = ctk.CTkFrame(

            self.pagina,

            fg_color="transparent"

        )

        inferior.pack(

            fill="x",

            padx=10,

            pady=10

        )

        inferior.grid_columnconfigure(

            0,

            weight=1

        )

        inferior.grid_columnconfigure(

            1,

            weight=2

        )

        # --------------------------------------------------
        # RESUMO
        # --------------------------------------------------

        self.criar_resumo_dashboard(

            inferior,

            total_orcamentos,

            aprovados,

            pendentes,

            recusados,

            concluidos,

            taxa_aprovacao

        ).grid(

            row=0,

            column=0,

            padx=8,

            sticky="nsew"

        )

        # --------------------------------------------------
        # ÚLTIMOS ORÇAMENTOS
        # --------------------------------------------------

        self.criar_ultimos_orcamentos(

            inferior,

            orcamentos

        ).grid(

            row=0,

            column=1,

            padx=8,

            sticky="nsew"

        )

    # ======================================================
    # CARD DO DASHBOARD
    # ======================================================

    def criar_card_dashboard(

        self,

        parent,

        icone,

        titulo,

        valor

    ):

        card = ctk.CTkFrame(

            parent,

            height=130,

            corner_radius=15,

            fg_color=COR_CARD,

            border_width=1,

            border_color=COR_BORDA

        )

        card.grid_propagate(

            False

        )

        ctk.CTkLabel(

            card,

            text=icone,

            font=(

                "Arial",

                25

            )

        ).pack(

            pady=(

                15,

                0

            )

        )

        ctk.CTkLabel(

            card,

            text=titulo,

            font=(

                "Arial",

                13

            ),

            text_color=COR_TEXTO_SECUNDARIO

        ).pack(

            pady=3

        )

        ctk.CTkLabel(

            card,

            text=valor,

            font=(

                "Arial",

                21,

                "bold"

            ),

            text_color=COR_PRINCIPAL

        ).pack()

        return card

    # ======================================================
    # GRÁFICO DE STATUS
    # ======================================================

    def criar_grafico_status(

        self,

        parent,

        pendentes,

        aprovados,

        recusados,

        concluidos

    ):

        valores = [

            pendentes,

            aprovados,

            recusados,

            concluidos

        ]

        nomes = [

            "Pendente",

            "Aprovado",

            "Recusado",

            "Concluído"

        ]

        # --------------------------------------------------
        # SE NÃO EXISTIREM DADOS
        # --------------------------------------------------

        if sum(valores) == 0:

            ctk.CTkLabel(

                parent,

                text="Nenhum orçamento cadastrado.",

                font=(

                    "Arial",

                    14

                ),

                text_color=COR_TEXTO_SECUNDARIO

            ).pack(

                pady=60

            )

            return

        # --------------------------------------------------
        # FIGURA
        # --------------------------------------------------

        figura = Figure(

            figsize=(

                4.5,

                3.2

            ),

            dpi=90

        )

        eixo = figura.add_subplot(

            111

        )

        eixo.pie(

            valores,

            labels=nomes,

            autopct="%1.0f%%",

            startangle=90,

            wedgeprops={

                "width": 0.42,

                "edgecolor": "white"

            }

        )

        eixo.set_title(

            "Status dos Orçamentos",

            fontsize=11

        )

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(

            figura,

            master=parent

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=5

        )

    # ======================================================
    # GRÁFICO DE VALORES
    # ======================================================

    def criar_grafico_valores(

        self,

        parent,

        orcamentos

    ):

        valores_status = {

            "Pendente": 0,

            "Aprovado": 0,

            "Recusado": 0,

            "Concluído": 0

        }

        for orcamento in orcamentos:

            status = str(

                orcamento["status"]

                or "Pendente"

            ).strip().lower()

            try:

                valor = float(

                    orcamento["valor_total"]

                    or 0

                )

            except (

                ValueError,

                TypeError

            ):

                valor = 0

            if status == "pendente":

                valores_status["Pendente"] += valor

            elif status == "aprovado":

                valores_status["Aprovado"] += valor

            elif status == "recusado":

                valores_status["Recusado"] += valor

            elif status in (

                "concluído",

                "concluido"

            ):

                valores_status["Concluído"] += valor

        if not orcamentos:

            ctk.CTkLabel(

                parent,

                text="Nenhum orçamento cadastrado.",

                font=(

                    "Arial",

                    14

                ),

                text_color=COR_TEXTO_SECUNDARIO

            ).pack(

                pady=60

            )

            return

        figura = Figure(

            figsize=(

                5,

                3.2

            ),

            dpi=90

        )

        eixo = figura.add_subplot(

            111

        )

        nomes = list(

            valores_status.keys()

        )

        valores = list(

            valores_status.values()

        )

        eixo.bar(

            nomes,

            valores

        )

        eixo.set_ylabel(

            "Valor (R$)"

        )

        eixo.tick_params(

            axis="x",

            rotation=15

        )

        eixo.grid(

            axis="y",

            alpha=0.2

        )

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(

            figura,

            master=parent

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=5

        )

    # ======================================================
    # RESUMO DO DASHBOARD
    # ======================================================

    def criar_resumo_dashboard(

        self,

        parent,

        total,

        aprovados,

        pendentes,

        recusados,

        concluidos,

        taxa

    ):

        frame = ctk.CTkFrame(

            parent,

            corner_radius=15,

            fg_color=COR_CARD,

            border_width=1,

            border_color=COR_BORDA

        )

        ctk.CTkLabel(

            frame,

            text="Resumo de Desempenho",

            font=(

                "Arial",

                17,

                "bold"

            ),

            text_color=COR_TEXTO

        ).pack(

            anchor="w",

            padx=20,

            pady=(

                20,

                15

            )

        )

        dados = [

            (

                "Total de Orçamentos",

                total

            ),

            (

                "Aprovados",

                aprovados

            ),

            (

                "Pendentes",

                pendentes

            ),

            (

                "Recusados",

                recusados

            ),

            (

                "Concluídos",

                concluidos

            ),

            (

                "Taxa de Aprovação",

                f"{taxa:.1f}%"

            )

        ]

        for nome, valor in dados:

            linha = ctk.CTkFrame(

                frame,

                fg_color="transparent"

            )

            linha.pack(

                fill="x",

                padx=20,

                pady=6

            )

            ctk.CTkLabel(

                linha,

                text=nome,

                font=(

                    "Arial",

                    13

                ),

                text_color=COR_TEXTO_SECUNDARIO

            ).pack(

                side="left"

            )

            ctk.CTkLabel(

                linha,

                text=str(valor),

                font=(

                    "Arial",

                    13,

                    "bold"

                ),

                text_color=COR_PRINCIPAL

            ).pack(

                side="right"

            )

        return frame

    # ======================================================
    # ÚLTIMOS ORÇAMENTOS
    # ======================================================

    def criar_ultimos_orcamentos(

        self,

        parent,

        orcamentos

    ):

        frame = ctk.CTkFrame(

            parent,

            corner_radius=15,

            fg_color=COR_CARD,

            border_width=1,

            border_color=COR_BORDA

        )

        ctk.CTkLabel(

            frame,

            text="Últimos Orçamentos",

            font=(

                "Arial",

                17,

                "bold"

            ),

            text_color=COR_TEXTO

        ).pack(

            anchor="w",

            padx=20,

            pady=(

                20,

                15

            )

        )

        ultimos = orcamentos[:6]

        if not ultimos:

            ctk.CTkLabel(

                frame,

                text="Nenhum orçamento cadastrado.",

                text_color=COR_TEXTO_SECUNDARIO

            ).pack(

                pady=30

            )

            return frame

        for orcamento in ultimos:

            linha = ctk.CTkFrame(

                frame,

                fg_color="#F8FAFC",

                corner_radius=8

            )

            linha.pack(

                fill="x",

                padx=15,

                pady=4

            )

            texto = (

                f"#{orcamento['id']}  "

                f"{orcamento['cliente_nome']}  |  "

                f"{orcamento['servico']}"

            )

            ctk.CTkLabel(

                linha,

                text=texto,

                font=(

                    "Arial",

                    12,

                    "bold"

                ),

                anchor="w"

            ).pack(

                side="left",

                padx=10,

                pady=8

            )

            ctk.CTkLabel(

                linha,

                text=formatar_moeda(

                    orcamento["valor_total"]

                ),

                font=(

                    "Arial",

                    11,

                    "bold"

                ),

                text_color=COR_PRINCIPAL

            ).pack(

                side="right",

                padx=10

            )

        return frame

    # ======================================================
    # ATUALIZAR DASHBOARD
    # ======================================================

    def atualizar_dashboard(self):

        self.abrir_dashboard()

    # ======================================================
    # CLIENTES
    # ======================================================

    def abrir_clientes(self):

        self.limpar_pagina()

        self.titulo.configure(

            text="Gerenciamento de Clientes"

        )

        topo = ctk.CTkFrame(

            self.pagina,

            fg_color="transparent"

        )

        topo.pack(

            fill="x",

            pady=10

        )

        # --------------------------------------------------
        # NOVO CLIENTE
        # --------------------------------------------------

        ctk.CTkButton(

            topo,

            text="+ Novo Cliente",

            width=160,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=self.abrir_formulario_cliente

        ).pack(

            side="left"

        )

        # --------------------------------------------------
        # PESQUISA
        # --------------------------------------------------

        self.campo_busca_cliente = ctk.CTkEntry(

            topo,

            placeholder_text=(

                "Pesquisar por nome ou telefone..."

            ),

            width=350

        )

        self.campo_busca_cliente.pack(

            side="right",

            padx=10

        )

        ctk.CTkButton(

            topo,

            text="🔍 Pesquisar",

            width=120,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=self.buscar_clientes_interface

        ).pack(

            side="right"

        )

        # --------------------------------------------------
        # LISTA
        # --------------------------------------------------

        self.lista_clientes_frame = (

            ctk.CTkScrollableFrame(

                self.pagina,

                fg_color="transparent"

            )

        )

        self.lista_clientes_frame.pack(

            fill="both",

            expand=True,

            pady=15

        )

        self.exibir_clientes()

    # ======================================================
    # FORMULÁRIO CLIENTE
    # ======================================================

    def abrir_formulario_cliente(

        self,

        cliente=None

    ):

        janela = ctk.CTkToplevel(

            self

        )

        janela.title(

            "Editar Cliente"

            if cliente

            else "Novo Cliente"

        )

        janela.geometry(

            "450x350"

        )

        janela.resizable(

            False,

            False

        )

        janela.grab_set()

        ctk.CTkLabel(

            janela,

            text=(

                "Editar Cliente"

                if cliente

                else "Cadastrar Cliente"

            ),

            font=(

                "Arial",

                24,

                "bold"

            )

        ).pack(

            pady=25

        )

        campo_nome = ctk.CTkEntry(

            janela,

            placeholder_text="Nome do cliente",

            width=350

        )

        campo_nome.pack(

            pady=10

        )

        campo_telefone = ctk.CTkEntry(

            janela,

            placeholder_text="Telefone",

            width=350

        )

        campo_telefone.pack(

            pady=10

        )

        if cliente:

            campo_nome.insert(

                0,

                cliente["nome"]

            )

            campo_telefone.insert(

                0,

                cliente["telefone"]

                or ""

            )

        def salvar():

            nome = (

                campo_nome

                .get()

                .strip()

            )

            telefone = (

                campo_telefone

                .get()

                .strip()

            )

            if cliente:

                sucesso, mensagem = editar_cliente(

                    cliente["id"],

                    nome,

                    telefone

                )

            else:

                sucesso, mensagem = cadastrar_cliente(

                    nome,

                    telefone

                )

            if sucesso:

                messagebox.showinfo(

                    "Sucesso",

                    mensagem

                )

                janela.destroy()

                self.abrir_clientes()

            else:

                messagebox.showerror(

                    "Erro",

                    mensagem

                )

        ctk.CTkButton(

            janela,

            text="Salvar",

            width=200,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=salvar

        ).pack(

            pady=25

        )

    # ======================================================
    # EXIBIR CLIENTES
    # ======================================================

    def exibir_clientes(

        self,

        clientes=None

    ):

        for widget in (

            self.lista_clientes_frame

            .winfo_children()

        ):

            widget.destroy()

        if clientes is None:

            clientes = listar_clientes()

        if not clientes:

            ctk.CTkLabel(

                self.lista_clientes_frame,

                text="Nenhum cliente encontrado.",

                font=(

                    "Arial",

                    18

                )

            ).pack(

                pady=30

            )

            return

        for cliente in clientes:

            frame = ctk.CTkFrame(

                self.lista_clientes_frame,

                corner_radius=10,

                fg_color=COR_CARD

            )

            frame.pack(

                fill="x",

                pady=5,

                padx=5

            )

            texto = (

                f"{cliente['nome']}  |  "

                f"{cliente['telefone'] or 'Sem telefone'}"

            )

            ctk.CTkLabel(

                frame,

                text=texto,

                font=(

                    "Arial",

                    15

                ),

                anchor="w"

            ).pack(

                side="left",

                padx=15,

                pady=15

            )

            ctk.CTkButton(

                frame,

                text="Excluir",

                width=80,

                command=lambda c=cliente:

                    self.confirmar_exclusao_cliente(c)

            ).pack(

                side="right",

                padx=5

            )

            ctk.CTkButton(

                frame,

                text="Editar",

                width=80,

                command=lambda c=cliente:

                    self.abrir_formulario_cliente(c)

            ).pack(

                side="right",

                padx=5

            )

    # ======================================================
    # PESQUISAR CLIENTES
    # ======================================================

    def buscar_clientes_interface(self):

        termo = (

            self.campo_busca_cliente

            .get()

        )

        clientes = pesquisar_clientes(

            termo

        )

        self.exibir_clientes(

            clientes

        )

    # ======================================================
    # EXCLUIR CLIENTE
    # ======================================================

    def confirmar_exclusao_cliente(

        self,

        cliente

    ):

        confirmar = messagebox.askyesno(

            "Confirmar exclusão",

            (

                f"Deseja excluir o cliente "

                f"'{cliente['nome']}'?"

            )

        )

        if not confirmar:

            return

        sucesso, mensagem = excluir_cliente(

            cliente["id"]

        )

        if sucesso:

            messagebox.showinfo(

                "Sucesso",

                mensagem

            )

            self.abrir_clientes()

        else:

            messagebox.showerror(

                "Não foi possível excluir",

                mensagem

            )

    # ======================================================
    # ORÇAMENTOS
    # ======================================================

    def abrir_orcamentos(self):

        self.limpar_pagina()

        self.titulo.configure(

            text="Gerenciamento de Orçamentos"

        )

        topo = ctk.CTkFrame(

            self.pagina,

            fg_color="transparent"

        )

        topo.pack(

            fill="x",

            pady=10

        )

        ctk.CTkButton(

            topo,

            text="+ Novo Orçamento",

            width=180,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=self.abrir_formulario_orcamento

        ).pack(

            side="left"

        )

        self.campo_busca_orcamento = ctk.CTkEntry(

            topo,

            placeholder_text=(

                "Cliente, telefone ou serviço..."

            ),

            width=350

        )

        self.campo_busca_orcamento.pack(

            side="right",

            padx=10

        )

        ctk.CTkButton(

            topo,

            text="🔍 Pesquisar",

            width=120,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=self.buscar_orcamentos_interface

        ).pack(

            side="right"

        )

        self.lista_orcamentos_frame = (

            ctk.CTkScrollableFrame(

                self.pagina,

                fg_color="transparent"

            )

        )

        self.lista_orcamentos_frame.pack(

            fill="both",

            expand=True,

            pady=15

        )

        self.exibir_orcamentos()

    # ======================================================
    # FORMULÁRIO ORÇAMENTO
    # ======================================================

    def abrir_formulario_orcamento(

        self,

        orcamento=None

    ):

        clientes = listar_clientes()

        if not clientes:

            messagebox.showwarning(

                "Atenção",

                (

                    "Nenhum cliente cadastrado.\n\n"

                    "Cadastre um cliente antes "

                    "de criar um orçamento."

                )

            )

            return

        janela = ctk.CTkToplevel(

            self

        )

        janela.title(

            "Editar Orçamento"

            if orcamento

            else "Novo Orçamento"

        )

        janela.geometry(

            "500x650"

        )

        janela.resizable(

            False,

            False

        )

        janela.grab_set()

        ctk.CTkLabel(

            janela,

            text=(

                "Editar Orçamento"

                if orcamento

                else "Novo Orçamento"

            ),

            font=(

                "Arial",

                24,

                "bold"

            )

        ).pack(

            pady=20

        )

        ctk.CTkLabel(

            janela,

            text="Cliente"

        ).pack()

        nomes_clientes = [

            f"{cliente['id']} - "

            f"{cliente['nome']}"

            for cliente in clientes

        ]

        combo_cliente = ctk.CTkComboBox(

            janela,

            values=nomes_clientes,

            width=350

        )

        combo_cliente.pack(

            pady=10

        )

        campo_servico = ctk.CTkEntry(

            janela,

            placeholder_text="Serviço",

            width=350

        )

        campo_servico.pack(

            pady=10

        )

        campo_area = ctk.CTkEntry(

            janela,

            placeholder_text="Área em m²",

            width=350

        )

        campo_area.pack(

            pady=10

        )

        campo_valor_m2 = ctk.CTkEntry(

            janela,

            placeholder_text="Valor por m²",

            width=350

        )

        campo_valor_m2.pack(

            pady=10

        )

        combo_status = ctk.CTkComboBox(

            janela,

            values=[

                "Pendente",

                "Aprovado",

                "Recusado",

                "Concluído"

            ],

            width=350

        )

        combo_status.pack(

            pady=10

        )

        combo_status.set(

            "Pendente"

        )

        label_total = ctk.CTkLabel(

            janela,

            text="Total: R$ 0,00",

            font=(

                "Arial",

                20,

                "bold"

            )

        )

        label_total.pack(

            pady=15

        )

        def atualizar_total(event=None):

            try:

                area = float(

                    campo_area

                    .get()

                    .replace(",", ".")

                )

                valor_m2 = float(

                    campo_valor_m2

                    .get()

                    .replace(",", ".")

                )

                total = (

                    area *

                    valor_m2

                )

                label_total.configure(

                    text=(

                        f"Total: "

                        f"{formatar_moeda(total)}"

                    )

                )

            except (

                ValueError,

                TypeError

            ):

                label_total.configure(

                    text="Total: R$ 0,00"

                )

        campo_area.bind(

            "<KeyRelease>",

            atualizar_total

        )

        campo_valor_m2.bind(

            "<KeyRelease>",

            atualizar_total

        )

        if orcamento:

            combo_cliente.set(

                f"{orcamento['cliente_id']} - "

                f"{orcamento['cliente_nome']}"

            )

            campo_servico.insert(

                0,

                orcamento["servico"]

            )

            campo_area.insert(

                0,

                str(orcamento["area"])

            )

            campo_valor_m2.insert(

                0,

                str(orcamento["valor_m2"])

            )

            combo_status.set(

                orcamento["status"]

            )

            atualizar_total()

        def salvar():

            try:

                cliente_id = int(

                    combo_cliente

                    .get()

                    .split(" - ")[0]

                )

            except (

                ValueError,

                IndexError

            ):

                messagebox.showerror(

                    "Erro",

                    "Selecione um cliente válido."

                )

                return

            servico = (

                campo_servico

                .get()

                .strip()

            )

            area = (

                campo_area

                .get()

                .replace(",", ".")

            )

            valor_m2 = (

                campo_valor_m2

                .get()

                .replace(",", ".")

            )

            status = combo_status.get()

            if orcamento:

                sucesso, mensagem = editar_orcamento(

                    orcamento["id"],

                    cliente_id,

                    servico,

                    area,

                    valor_m2,

                    status

                )

            else:

                sucesso, mensagem = cadastrar_orcamento(

                    cliente_id,

                    servico,

                    area,

                    valor_m2,

                    status

                )

            if sucesso:

                messagebox.showinfo(

                    "Sucesso",

                    mensagem

                )

                janela.destroy()

                self.abrir_orcamentos()

            else:

                messagebox.showerror(

                    "Erro",

                    mensagem

                )

        ctk.CTkButton(

            janela,

            text="Salvar Orçamento",

            width=220,

            fg_color=COR_PRINCIPAL,

            hover_color=COR_SECUNDARIA,

            command=salvar

        ).pack(

            pady=20

        )

            # ======================================================
    # EXIBIR ORÇAMENTOS
    # ======================================================

    def exibir_orcamentos(self, orcamentos=None):

        for widget in self.lista_orcamentos_frame.winfo_children():
            widget.destroy()

        if orcamentos is None:
            orcamentos = listar_orcamentos()

        if not orcamentos:

            ctk.CTkLabel(
                self.lista_orcamentos_frame,
                text="Nenhum orçamento encontrado.",
                font=("Arial", 18)
            ).pack(pady=30)

            return

        for orcamento in orcamentos:

            frame = ctk.CTkFrame(
                self.lista_orcamentos_frame
            )

            frame.pack(
                fill="x",
                pady=5,
                padx=5
            )

            texto = (
                f"#{orcamento['id']} | "
                f"{orcamento['cliente_nome']} | "
                f"{orcamento['servico']} | "
                f"{formatar_numero(orcamento['area'])} m² | "
                f"{formatar_moeda(orcamento['valor_total'])} | "
                f"{orcamento['status']}"
            )

            ctk.CTkLabel(
                frame,
                text=texto,
                font=("Arial", 14),
                anchor="w"
            ).pack(
                side="left",
                padx=10,
                pady=15
            )

            ctk.CTkButton(
                frame,
                text="📄 PDF",
                width=90,
                command=lambda o=orcamento:
                    self.gerar_pdf_interface(o)
            ).pack(
                side="right",
                padx=5
            )

            ctk.CTkButton(
                frame,
                text="Excluir",
                width=80,
                command=lambda o=orcamento:
                    self.confirmar_exclusao_orcamento(o)
            ).pack(
                side="right",
                padx=5
            )

            ctk.CTkButton(
                frame,
                text="Editar",
                width=80,
                command=lambda o=orcamento:
                    self.abrir_formulario_orcamento(o)
            ).pack(
                side="right",
                padx=5
            )


    # ======================================================
    # PESQUISAR ORÇAMENTOS
    # ======================================================

    def buscar_orcamentos_interface(self):

        termo = self.campo_busca_orcamento.get()

        orcamentos = pesquisar_orcamentos(
            termo
        )

        self.exibir_orcamentos(
            orcamentos
        )


    # ======================================================
    # EXCLUIR ORÇAMENTO
    # ======================================================

    def confirmar_exclusao_orcamento(
        self,
        orcamento
    ):

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            (
                f"Deseja excluir o orçamento "
                f"#{orcamento['id']}?"
            )
        )

        if not confirmar:
            return

        sucesso, mensagem = excluir_orcamento(
            orcamento["id"]
        )

        if sucesso:

            messagebox.showinfo(
                "Sucesso",
                mensagem
            )

            self.abrir_orcamentos()

        else:

            messagebox.showerror(
                "Erro",
                mensagem
            )


    # ======================================================
    # GERAR PDF
    # ======================================================

    def gerar_pdf_interface(
        self,
        orcamento
    ):

        try:

            dados = buscar_orcamento(
                orcamento["id"]
            )

            if dados is None:

                messagebox.showerror(
                    "Erro",
                    "Orçamento não encontrado."
                )

                return

            if isinstance(
                dados,
                dict
            ):

                orcamento_dict = dados

            else:

                orcamento_dict = dict(
                    dados
                )

            sucesso, resultado = gerar_pdf_orcamento(
                orcamento_dict
            )

            if sucesso:

                messagebox.showinfo(
                    "PDF gerado com sucesso",
                    (
                        "O PDF do orçamento foi "
                        "gerado com sucesso!\n\n"
                        f"Arquivo:\n{resultado}"
                    )
                )

            else:

                messagebox.showerror(
                    "Erro ao gerar PDF",
                    resultado
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao gerar PDF",
                (
                    "Não foi possível gerar o PDF.\n\n"
                    f"Erro: {erro}"
                )
            )


    # ======================================================
    # RELATÓRIOS
    # ======================================================

    def abrir_relatorios(self):

        self.limpar_pagina()

        self.titulo.configure(
            text="Relatórios"
        )

        ctk.CTkLabel(
            self.pagina,
            text=(
                "Módulo de relatórios\n\n"
                "Use o botão PDF na tela de "
                "orçamentos para gerar o documento."
            ),
            font=("Arial", 20)
        ).pack(
            pady=50
        )


    # ======================================================
    # CONFIGURAÇÕES
    # ======================================================

    def abrir_configuracoes(self):

        self.limpar_pagina()

        self.titulo.configure(
            text="Configurações"
        )

        ctk.CTkLabel(
            self.pagina,
            text=(
                "FS ART Gesso & Drywall\n\n"
                "Sistema OrçaSmart\n\n"
                "Desenvolvido por "
                "Frank Correia Souza"
            ),
            font=("Arial", 20)
        ).pack(
            pady=50
        )


# ==========================================================
# EXECUÇÃO DIRETA
# ==========================================================

if __name__ == "__main__":

    app = Sistema()

    app.mainloop()