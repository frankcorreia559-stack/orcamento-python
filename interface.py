import customtkinter as ctk
from tkinter import messagebox

from banco import (
    criar_tabelas,
    migrar_banco,
    cadastrar_cliente as db_cadastrar_cliente,
    listar_clientes,
    buscar_clientes,
    editar_cliente,
    excluir_cliente,
    cadastrar_orcamento as db_cadastrar_orcamento,
    listar_orcamentos,
    buscar_orcamentos,
    excluir_orcamento,
    obter_estatisticas
)

from gerar_pdf import gerar_pdf_orcamento


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==========================================================
# CLASSE PRINCIPAL
# ==========================================================

class Sistema(ctk.CTk):

    def __init__(self, usuario_logado=None):

        super().__init__()

        # --------------------------------------------------
        # INICIALIZAR BANCO
        # --------------------------------------------------

        criar_tabelas()
        migrar_banco()

        # --------------------------------------------------
        # USUÁRIO LOGADO
        # --------------------------------------------------

        self.usuario_logado = usuario_logado

        if self.usuario_logado:

            self.usuario_id = self.usuario_logado["id"]

            self.nome_usuario = (
                self.usuario_logado["nome"]
            )

            self.login_usuario = (
                self.usuario_logado["usuario"]
            )

        else:

            self.usuario_id = None

            self.nome_usuario = "Usuário"

            self.login_usuario = ""


        # --------------------------------------------------
        # CONFIGURAÇÃO DA JANELA
        # --------------------------------------------------

        self.title(
            "OrçaSmart - Sistema de Orçamentos"
        )

        self.geometry(
            "1200x700"
        )

        self.minsize(
            1000,
            600
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )


        # --------------------------------------------------
        # CRIAR INTERFACE
        # --------------------------------------------------

        self.criar_menu_lateral()

        self.criar_area_principal()

        self.mostrar_dashboard()


    # ======================================================
    # MENU LATERAL
    # ======================================================

    def criar_menu_lateral(self):

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.menu_lateral.grid_propagate(
            False
        )


        ctk.CTkLabel(
            self.menu_lateral,
            text="OrçaSmart",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=(40, 5)
        )


        ctk.CTkLabel(
            self.menu_lateral,
            text="Sistema de Orçamentos",
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            pady=(0, 30)
        )


        # --------------------------------------------------
        # USUÁRIO LOGADO
        # --------------------------------------------------

        usuario_frame = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent"
        )

        usuario_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        ctk.CTkLabel(
            usuario_frame,
            text="Usuário conectado",
            font=ctk.CTkFont(
                size=11
            )
        ).pack()


        ctk.CTkLabel(
            usuario_frame,
            text=self.nome_usuario,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack()


        ctk.CTkLabel(
            usuario_frame,
            text=f"@{self.login_usuario}",
            font=ctk.CTkFont(
                size=10
            )
        ).pack()


        # --------------------------------------------------
        # BOTÕES
        # --------------------------------------------------

        self.btn_dashboard = ctk.CTkButton(
            self.menu_lateral,
            text="📊  Dashboard",
            height=45,
            anchor="w",
            command=self.mostrar_dashboard
        )

        self.btn_dashboard.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        self.btn_clientes = ctk.CTkButton(
            self.menu_lateral,
            text="👤  Clientes",
            height=45,
            anchor="w",
            command=self.abrir_clientes
        )

        self.btn_clientes.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        self.btn_orcamentos = ctk.CTkButton(
            self.menu_lateral,
            text="📋  Orçamentos",
            height=45,
            anchor="w",
            command=self.abrir_orcamentos
        )

        self.btn_orcamentos.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        self.btn_relatorios = ctk.CTkButton(
            self.menu_lateral,
            text="📈  Relatórios",
            height=45,
            anchor="w",
            command=self.abrir_relatorios
        )

        self.btn_relatorios.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        self.btn_configuracoes = ctk.CTkButton(
            self.menu_lateral,
            text="⚙️  Configurações",
            height=45,
            anchor="w",
            command=self.abrir_configuracoes
        )

        self.btn_configuracoes.pack(
            padx=20,
            pady=5,
            fill="x"
        )


        ctk.CTkLabel(
            self.menu_lateral,
            text=""
        ).pack(
            expand=True
        )


        ctk.CTkLabel(
            self.menu_lateral,
            text="OrçaSmart\nVersão 1.0",
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            pady=20
        )


    # ======================================================
    # ÁREA PRINCIPAL
    # ======================================================

    def criar_area_principal(self):

        self.area_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )


    # ======================================================
    # LIMPAR ÁREA
    # ======================================================

    def limpar_area(self):

        for widget in self.area_principal.winfo_children():

            widget.destroy()


    # ======================================================
    # DASHBOARD
    # ======================================================

    def mostrar_dashboard(self):

        self.limpar_area()


        estatisticas = obter_estatisticas(
            self.usuario_id
        )


        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        cabecalho = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )

        cabecalho.pack(
            fill="x",
            pady=(10, 30)
        )


        ctk.CTkLabel(
            cabecalho,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )


        ctk.CTkLabel(
            cabecalho,
            text=(
                f"Olá, {self.nome_usuario}! "
                "Bem-vindo ao OrçaSmart."
            ),
            font=ctk.CTkFont(
                size=15
            )
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # --------------------------------------------------
        # CARDS
        # --------------------------------------------------

        cards = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )

        cards.pack(
            fill="x"
        )


        cards.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        self.criar_card(
            cards,
            0,
            "👤",
            "Clientes",
            estatisticas["clientes"]
        )


        self.criar_card(
            cards,
            1,
            "📋",
            "Orçamentos",
            estatisticas["orcamentos"]
        )


        valor = (
            f"R$ {estatisticas['valor_total']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


        self.criar_card(
            cards,
            2,
            "💰",
            "Valor Total",
            valor
        )


    # ======================================================
    # CRIAR CARD
    # ======================================================

    def criar_card(
        self,
        container,
        coluna,
        icone,
        titulo,
        valor
    ):

        card = ctk.CTkFrame(
            container,
            height=150
        )


        card.grid(
            row=0,
            column=coluna,
            padx=10,
            pady=10,
            sticky="nsew"
        )


        card.grid_propagate(
            False
        )


        ctk.CTkLabel(
            card,
            text=icone,
            font=ctk.CTkFont(
                size=35
            )
        ).pack(
            pady=(20, 5)
        )


        ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack()


        ctk.CTkLabel(
            card,
            text=str(valor),
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            pady=5
        )


    # ======================================================
    # CLIENTES
    # ======================================================

    def abrir_clientes(self):

        self.limpar_area()


        titulo = ctk.CTkLabel(
            self.area_principal,
            text="Clientes",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            pady=(10, 20)
        )


        barra = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )

        barra.pack(
            fill="x",
            pady=10
        )


        ctk.CTkButton(
            barra,
            text="+ Novo Cliente",
            width=180,
            height=40,
            command=self.cadastrar_cliente
        ).pack(
            side="left"
        )


        self.entry_busca_cliente = ctk.CTkEntry(
            barra,
            placeholder_text="Pesquisar cliente..."
        )

        self.entry_busca_cliente.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10)
        )


        ctk.CTkButton(
            barra,
            text="Pesquisar",
            width=120,
            command=self.pesquisar_clientes
        ).pack(
            side="left"
        )


        self.lista_clientes = ctk.CTkTextbox(
            self.area_principal
        )

        self.lista_clientes.pack(
            fill="both",
            expand=True,
            pady=10
        )


        self.atualizar_lista_clientes()


    # ======================================================
    # ATUALIZAR CLIENTES
    # ======================================================

    def atualizar_lista_clientes(
        self,
        clientes=None
    ):

        if clientes is None:

            clientes = listar_clientes(
                self.usuario_id
            )


        self.clientes_exibidos = list(
            clientes
        )


        self.lista_clientes.configure(
            state="normal"
        )


        self.lista_clientes.delete(
            "1.0",
            "end"
        )


        if not self.clientes_exibidos:

            self.lista_clientes.insert(
                "end",
                "Nenhum cliente cadastrado."
            )


        else:

            for indice, cliente in enumerate(
                self.clientes_exibidos
            ):

                texto = (
                    f"[{indice + 1}]  "
                    f"ID: {cliente['id']}\n"
                    f"Nome: {cliente['nome']}\n"
                    f"Telefone: "
                    f"{cliente['telefone'] or 'Não informado'}\n"
                    f"{'-' * 70}\n"
                )


                self.lista_clientes.insert(
                    "end",
                    texto
                )


        self.lista_clientes.configure(
            state="disabled"
        )


    # ======================================================
    # PESQUISAR CLIENTES
    # ======================================================

    def pesquisar_clientes(self):

        nome = (
            self.entry_busca_cliente
            .get()
            .strip()
        )


        if nome:

            clientes = buscar_clientes(
                self.usuario_id,
                nome
            )


        else:

            clientes = listar_clientes(
                self.usuario_id
            )


        self.atualizar_lista_clientes(
            clientes
        )


    # ======================================================
    # CADASTRAR CLIENTE
    # ======================================================

    def cadastrar_cliente(self):

        janela = ctk.CTkToplevel(
            self
        )


        janela.title(
            "Cadastrar Cliente"
        )


        janela.geometry(
            "450x350"
        )


        janela.grab_set()


        ctk.CTkLabel(
            janela,
            text="Novo Cliente",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=20
        )


        entry_nome = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do cliente",
            width=350
        )


        entry_nome.pack(
            pady=10
        )


        entry_telefone = ctk.CTkEntry(
            janela,
            placeholder_text="Telefone",
            width=350
        )


        entry_telefone.pack(
            pady=10
        )


        def salvar():

            nome = (
                entry_nome
                .get()
                .strip()
            )


            telefone = (
                entry_telefone
                .get()
                .strip()
            )


            sucesso, mensagem = (
                db_cadastrar_cliente(
                    self.usuario_id,
                    nome,
                    telefone
                )
            )


            if sucesso:

                messagebox.showinfo(
                    "Sucesso",
                    mensagem,
                    parent=janela
                )


                janela.destroy()


                self.abrir_clientes()


            else:

                messagebox.showerror(
                    "Erro",
                    mensagem,
                    parent=janela
                )


        ctk.CTkButton(
            janela,
            text="Salvar Cliente",
            width=200,
            height=40,
            command=salvar
        ).pack(
            pady=30
        )


    # ======================================================
    # ORÇAMENTOS
    # ======================================================

    def abrir_orcamentos(self):

        self.limpar_area()


        titulo = ctk.CTkLabel(
            self.area_principal,
            text="Orçamentos",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )


        titulo.pack(
            anchor="w",
            pady=(10, 20)
        )


        barra = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )


        barra.pack(
            fill="x",
            pady=10
        )


        ctk.CTkButton(
            barra,
            text="+ Novo Orçamento",
            width=180,
            height=40,
            command=self.cadastrar_orcamento
        ).pack(
            side="left"
        )


        self.entry_busca_orcamento = ctk.CTkEntry(
            barra,
            placeholder_text="Pesquisar por cliente..."
        )


        self.entry_busca_orcamento.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10)
        )


        ctk.CTkButton(
            barra,
            text="Pesquisar",
            width=120,
            command=self.pesquisar_orcamentos
        ).pack(
            side="left"
        )


        self.lista_orcamentos = ctk.CTkTextbox(
            self.area_principal
        )


        self.lista_orcamentos.pack(
            fill="both",
            expand=True,
            pady=10
        )


        botoes = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent"
        )


        botoes.pack(
            fill="x",
            pady=5
        )


        ctk.CTkButton(
            botoes,
            text="📄 Gerar PDF do Orçamento",
            height=40,
            command=self.gerar_pdf_selecionado
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            botoes,
            text="🗑 Excluir Orçamento",
            height=40,
            command=self.excluir_orcamento_selecionado
        ).pack(
            side="left",
            padx=5
        )


        self.atualizar_lista_orcamentos()


    # ======================================================
    # ATUALIZAR ORÇAMENTOS
    # ======================================================

    def atualizar_lista_orcamentos(
        self,
        orcamentos=None
    ):

        if orcamentos is None:

            orcamentos = listar_orcamentos(
                self.usuario_id
            )


        self.orcamentos_exibidos = list(
            orcamentos
        )


        self.lista_orcamentos.configure(
            state="normal"
        )


        self.lista_orcamentos.delete(
            "1.0",
            "end"
        )


        if not self.orcamentos_exibidos:

            self.lista_orcamentos.insert(
                "end",
                "Nenhum orçamento cadastrado."
            )


        else:

            for indice, orcamento in enumerate(
                self.orcamentos_exibidos
            ):

                valor_total = float(
                    orcamento["valor_total"] or 0
                )


                valor_m2 = float(
                    orcamento["valor_m2"] or 0
                )


                valor_total_formatado = (
                    f"R$ {valor_total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )


                valor_m2_formatado = (
                    f"R$ {valor_m2:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )


                texto = (
                    f"[{indice + 1}]  "
                    f"ID: {orcamento['id']}\n"
                    f"Cliente: "
                    f"{orcamento['cliente']}\n"
                    f"Serviço: "
                    f"{orcamento['servico']}\n"
                    f"Área: "
                    f"{orcamento['area']} m²\n"
                    f"Valor por m²: "
                    f"{valor_m2_formatado}\n"
                    f"Valor Total: "
                    f"{valor_total_formatado}\n"
                    f"Status: "
                    f"{orcamento['status']}\n"
                    f"Data: "
                    f"{orcamento['data_criacao']}\n"
                    f"{'-' * 80}\n"
                )


                self.lista_orcamentos.insert(
                    "end",
                    texto
                )


        self.lista_orcamentos.configure(
            state="disabled"
        )


    # ======================================================
    # PESQUISAR ORÇAMENTOS
    # ======================================================

    def pesquisar_orcamentos(self):

        cliente = (
            self.entry_busca_orcamento
            .get()
            .strip()
        )


        if cliente:

            orcamentos = buscar_orcamentos(
                self.usuario_id,
                cliente
            )


        else:

            orcamentos = listar_orcamentos(
                self.usuario_id
            )


        self.atualizar_lista_orcamentos(
            orcamentos
        )


    # ======================================================
    # CADASTRAR ORÇAMENTO
    # ======================================================

    def cadastrar_orcamento(self):

        janela = ctk.CTkToplevel(
            self
        )


        janela.title(
            "Novo Orçamento"
        )


        janela.geometry(
            "500x550"
        )


        janela.grab_set()


        ctk.CTkLabel(
            janela,
            text="Novo Orçamento",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=20
        )


        entry_cliente = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do cliente",
            width=400
        )


        entry_cliente.pack(
            pady=8
        )


        entry_servico = ctk.CTkEntry(
            janela,
            placeholder_text="Descrição do serviço",
            width=400
        )


        entry_servico.pack(
            pady=8
        )


        entry_area = ctk.CTkEntry(
            janela,
            placeholder_text="Área em m²",
            width=400
        )


        entry_area.pack(
            pady=8
        )


        entry_valor = ctk.CTkEntry(
            janela,
            placeholder_text="Valor por m²",
            width=400
        )


        entry_valor.pack(
            pady=8
        )


        resultado = ctk.CTkLabel(
            janela,
            text="Valor total: R$ 0,00",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )


        resultado.pack(
            pady=20
        )


        def calcular():

            try:

                area = float(
                    entry_area
                    .get()
                    .replace(",", ".")
                )


                valor_m2 = float(
                    entry_valor
                    .get()
                    .replace(",", ".")
                )


                if area <= 0 or valor_m2 <= 0:

                    raise ValueError


                total = (
                    area
                    * valor_m2
                )


                total_formatado = (
                    f"R$ {total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )


                resultado.configure(
                    text=(
                        f"Valor total: "
                        f"{total_formatado}"
                    )
                )


                return (
                    area,
                    valor_m2
                )


            except ValueError:

                messagebox.showerror(
                    "Erro",
                    "Digite valores numéricos válidos.",
                    parent=janela
                )


                return None


        def salvar():

            cliente = (
                entry_cliente
                .get()
                .strip()
            )


            servico = (
                entry_servico
                .get()
                .strip()
            )


            if not cliente:

                messagebox.showwarning(
                    "Atenção",
                    "Digite o nome do cliente.",
                    parent=janela
                )


                return


            if not servico:

                messagebox.showwarning(
                    "Atenção",
                    "Digite a descrição do serviço.",
                    parent=janela
                )


                return


            valores = calcular()


            if valores is None:

                return


            area, valor_m2 = valores


            sucesso, mensagem = (
                db_cadastrar_orcamento(
                    self.usuario_id,
                    cliente,
                    servico,
                    area,
                    valor_m2
                )
            )


            if sucesso:

                messagebox.showinfo(
                    "Sucesso",
                    mensagem,
                    parent=janela
                )


                janela.destroy()


                self.abrir_orcamentos()


            else:

                messagebox.showerror(
                    "Erro",
                    mensagem,
                    parent=janela
                )


        ctk.CTkButton(
            janela,
            text="Calcular Orçamento",
            width=220,
            height=40,
            command=calcular
        ).pack(
            pady=10
        )


        ctk.CTkButton(
            janela,
            text="Salvar Orçamento",
            width=220,
            height=40,
            command=salvar
        ).pack(
            pady=10
        )


    # ======================================================
    # OBTER ORÇAMENTO SELECIONADO
    # ======================================================

    def obter_orcamento_selecionado(self):

        if not self.orcamentos_exibidos:

            messagebox.showwarning(
                "Atenção",
                "Não existem orçamentos cadastrados."
            )

            return None


        dialogo = ctk.CTkToplevel(
            self
        )


        dialogo.title(
            "Selecionar Orçamento"
        )


        dialogo.geometry(
            "500x450"
        )


        dialogo.grab_set()


        ctk.CTkLabel(
            dialogo,
            text="Selecione o orçamento",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            pady=20
        )


        selecionado = {
            "orcamento": None
        }


        for indice, orcamento in enumerate(
            self.orcamentos_exibidos
        ):

            valor = float(
                orcamento["valor_total"] or 0
            )


            valor_formatado = (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )


            texto = (
                f"#{indice + 1} - "
                f"{orcamento['cliente']} - "
                f"{orcamento['servico']} - "
                f"{valor_formatado}"
            )


            def selecionar(
                item=orcamento
            ):

                selecionado[
                    "orcamento"
                ] = item


                dialogo.destroy()


            ctk.CTkButton(
                dialogo,
                text=texto,
                anchor="w",
                command=selecionar
            ).pack(
                fill="x",
                padx=20,
                pady=5
            )


        self.wait_window(
            dialogo
        )


        return selecionado[
            "orcamento"
        ]


    # ======================================================
    # GERAR PDF
    # ======================================================

    def gerar_pdf_selecionado(self):

        orcamento = (
            self.obter_orcamento_selecionado()
        )


        if not orcamento:

            return


        sucesso, resultado = (
            gerar_pdf_orcamento(
                orcamento
            )
        )


        if sucesso:

            messagebox.showinfo(
                "PDF Gerado",
                (
                    "Orçamento gerado com sucesso!\n\n"
                    f"Arquivo:\n{resultado}"
                )
            )


        else:

            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível gerar o PDF.\n\n"
                    f"{resultado}"
                )
            )


    # ======================================================
    # EXCLUIR ORÇAMENTO
    # ======================================================

    def excluir_orcamento_selecionado(self):

        orcamento = (
            self.obter_orcamento_selecionado()
        )


        if not orcamento:

            return


        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            (
                f"Deseja excluir o orçamento "
                f"Nº {orcamento['id']}?"
            )
        )


        if not confirmar:

            return


        sucesso, mensagem = (
            excluir_orcamento(
                self.usuario_id,
                orcamento["id"]
            )
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
    # RELATÓRIOS
    # ======================================================

    def abrir_relatorios(self):

        self.limpar_area()


        titulo = ctk.CTkLabel(
            self.area_principal,
            text="Relatórios",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )


        titulo.pack(
            anchor="w",
            pady=(10, 20)
        )


        estatisticas = obter_estatisticas(
            self.usuario_id
        )


        valor_formatado = (
            f"R$ {estatisticas['valor_total']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


        texto = (
            f"Usuário: "
            f"{self.nome_usuario}\n\n"

            f"Total de clientes: "
            f"{estatisticas['clientes']}\n\n"

            f"Total de orçamentos: "
            f"{estatisticas['orcamentos']}\n\n"

            f"Valor total dos orçamentos: "
            f"{valor_formatado}"
        )


        ctk.CTkLabel(
            self.area_principal,
            text=texto,
            font=ctk.CTkFont(
                size=18
            ),
            justify="left"
        ).pack(
            anchor="w",
            pady=20
        )


    # ======================================================
    # CONFIGURAÇÕES
    # ======================================================

    def abrir_configuracoes(self):

        self.limpar_area()


        titulo = ctk.CTkLabel(
            self.area_principal,
            text="Configurações",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )


        titulo.pack(
            anchor="w",
            pady=(10, 20)
        )


        ctk.CTkLabel(
            self.area_principal,
            text=(
                f"Usuário conectado: "
                f"{self.nome_usuario}"
            ),
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(10, 20)
        )


        ctk.CTkLabel(
            self.area_principal,
            text="Aparência do sistema:",
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            anchor="w",
            pady=(20, 5)
        )


        modo = ctk.CTkOptionMenu(
            self.area_principal,
            values=[
                "Light",
                "Dark",
                "System"
            ],
            command=self.alterar_aparencia
        )


        modo.set(
            "Light"
        )


        modo.pack(
            anchor="w"
        )


    # ======================================================
    # ALTERAR APARÊNCIA
    # ======================================================

    def alterar_aparencia(
        self,
        escolha
    ):

        ctk.set_appearance_mode(
            escolha
        )


# ==========================================================
# EXECUTAR SISTEMA
# ==========================================================

if __name__ == "__main__":

    app = Sistema()

    app.mainloop()