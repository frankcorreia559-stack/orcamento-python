import customtkinter as ctk
import sqlite3
import os
from PIL import Image


# ==========================================================
# CONFIGURAÇÕES DO CUSTOMTKINTER
# ==========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Sistema(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CONFIGURAÇÕES DA JANELA
        # ==================================================

        self.title("OrçaSmart")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # ==================================================
        # MENU LATERAL
        # ==================================================

        self.menu = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        # Impede o menu de diminuir
        self.menu.pack_propagate(False)

        # ==================================================
        # NOME DO SISTEMA
        # ==================================================

        self.logo_nome = ctk.CTkLabel(
            self.menu,
            text="OrçaSmart",
            font=("Arial", 26, "bold")
        )

        self.logo_nome.pack(
            pady=(30, 40)
        )

        # ==================================================
        # BOTÕES DO MENU
        # ==================================================

        botoes = [
            "🏠 Dashboard",
            "👤 Clientes",
            "📋 Orçamentos",
            "📄 Relatórios",
            "⚙ Configurações"
        ]

        for texto in botoes:

            botao = ctk.CTkButton(
                self.menu,
                text=texto,
                width=180,
                height=45,
                font=("Arial", 14)
            )

            botao.pack(
                pady=8
            )

            # -------------------------------
            # DASHBOARD
            # -------------------------------

            if texto == "🏠 Dashboard":

                botao.configure(
                    command=self.abrir_dashboard
                )

            # -------------------------------
            # CLIENTES
            # -------------------------------

            elif texto == "👤 Clientes":

                botao.configure(
                    command=self.abrir_clientes
                )

        # ==================================================
        # ÁREA PRINCIPAL
        # ==================================================

        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="white"
        )

        self.conteudo.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==================================================
        # CARREGAR LOGO
        # ==================================================

        caminho_logo = os.path.join(
            os.path.dirname(__file__),
            "logo_orcamento.png"
        )

        print("Caminho da logo:", caminho_logo)
        print("Logo existe?", os.path.exists(caminho_logo))
        # ==================================================
        # LOGO DE FUNDO
        # ==================================================

        if os.path.exists(caminho_logo):

            imagem_original = Image.open(caminho_logo)

            self.logo_fundo_imagem = ctk.CTkImage(
                light_image=imagem_original,
                dark_image=imagem_original,
                size=(500, 300)
             )

            self.logo_fundo = ctk.CTkLabel(
                self.conteudo,
                text="",
                image=self.logo_fundo_imagem
            )

            self.logo_fundo.place(
                relx=0.5,
                rely=0.55,
                anchor="center"
            )

        else:

            print(
                "ERRO: A imagem logo_orcamento.png não foi encontrada."
            )

        # ==================================================
        # TÍTULO DO DASHBOARD
        # ==================================================

        self.titulo = ctk.CTkLabel(
            self.conteudo,
            text="Bem-vindo ao OrçaSmart",
            font=("Arial", 28, "bold"),
            text_color="#222222"
        )

        self.titulo.place(
            relx=0.5,
            rely=0.10,
            anchor="center"
        )

        # ==================================================
        # FRAME PARA AS PÁGINAS
        # ==================================================

        self.pagina = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent",
            corner_radius=0
        )

        self.pagina.place(
            relx=0,
            rely=0.18,
            relwidth=1,
            relheight=0.82
        )


    # ======================================================
    # DASHBOARD
    # ======================================================

    def abrir_dashboard(self):

        # Limpa somente o conteúdo da página
        for widget in self.pagina.winfo_children():

            widget.destroy()

        # Mostra novamente o título
        self.titulo.configure(
            text="Bem-vindo ao OrçaSmart"
        )

        # ==================================================
        # TEXTO DO DASHBOARD
        # ==================================================

        mensagem = ctk.CTkLabel(
            self.pagina,
            text=(
                "Sistema de gerenciamento de orçamentos\n\n"
                "Selecione uma opção no menu lateral."
            ),
            font=("Arial", 20),
            text_color="#333333"
        )

        mensagem.pack(
            pady=50
        )


    # ======================================================
    # TELA DE CLIENTES
    # ======================================================

    def abrir_clientes(self):

        # Limpa somente a página
        # NÃO limpa self.conteudo
        # Portanto, a logo continua existindo no fundo

        for widget in self.pagina.winfo_children():

            widget.destroy()

        # ==================================================
        # ALTERA O TÍTULO
        # ==================================================

        self.titulo.configure(
            text="Cadastro de Clientes"
        )

        # ==================================================
        # CAMPO NOME
        # ==================================================

        campo_nome = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Digite o nome do cliente",
            width=400,
            height=40
        )

        campo_nome.pack(
            pady=10
        )

        # ==================================================
        # CAMPO TELEFONE
        # ==================================================

        campo_telefone = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Digite o telefone",
            width=400,
            height=40
        )

        campo_telefone.pack(
            pady=10
        )

        # ==================================================
        # BOTÃO CADASTRAR
        # ==================================================

        botao_cadastrar = ctk.CTkButton(
            self.pagina,
            text="Cadastrar Cliente",
            width=200,
            height=40,
            command=lambda: self.cadastrar_cliente(
                campo_nome,
                campo_telefone
            )
        )

        botao_cadastrar.pack(
            pady=15
        )

        # ==================================================
        # BOTÃO LISTAR
        # ==================================================

        botao_listar = ctk.CTkButton(
            self.pagina,
            text="Listar Clientes",
            width=200,
            height=40,
            command=self.listar_clientes
        )

        botao_listar.pack(
            pady=10
        )


    # ======================================================
    # CADASTRAR CLIENTE
    # ======================================================

    def cadastrar_cliente(
        self,
        campo_nome,
        campo_telefone
    ):

        nome = campo_nome.get().strip()

        telefone = campo_telefone.get().strip()

        # ==================================================
        # VALIDAÇÃO
        # ==================================================

        if nome == "":

            print(
                "Digite o nome do cliente!"
            )

            return

        # ==================================================
        # CONECTAR AO BANCO
        # ==================================================

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        # ==================================================
        # CRIAR TABELA
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                telefone TEXT

            )
        """)

        # ==================================================
        # INSERIR CLIENTE
        # ==================================================

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

        # ==================================================
        # SALVAR
        # ==================================================

        conexao.commit()

        conexao.close()

        print(
            "Cliente cadastrado com sucesso!"
        )

        # ==================================================
        # LIMPAR CAMPOS
        # ==================================================

        campo_nome.delete(
            0,
            "end"
        )

        campo_telefone.delete(
            0,
            "end"
        )


    # ======================================================
    # LISTAR CLIENTES
    # ======================================================

    def listar_clientes(self):

        # ==================================================
        # LIMPAR PÁGINA
        # ==================================================

        for widget in self.pagina.winfo_children():

            widget.destroy()

        # ==================================================
        # TÍTULO
        # ==================================================

        self.titulo.configure(
            text="Clientes Cadastrados"
        )

        # ==================================================
        # CONECTAR AO BANCO
        # ==================================================

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        # ==================================================
        # GARANTIR QUE A TABELA EXISTE
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome TEXT NOT NULL,

                telefone TEXT

            )
        """)

        # ==================================================
        # BUSCAR CLIENTES
        # ==================================================

        cursor.execute("""
            SELECT
                id,
                nome,
                telefone

            FROM clientes

            ORDER BY nome
        """)

        clientes = cursor.fetchall()

        conexao.close()

        # ==================================================
        # NENHUM CLIENTE
        # ==================================================

        if not clientes:

            mensagem = ctk.CTkLabel(
                self.pagina,
                text="Nenhum cliente cadastrado.",
                font=("Arial", 18)
            )

            mensagem.pack(
                pady=30
            )

            return

        # ==================================================
        # EXIBIR CLIENTES
        # ==================================================

        for cliente in clientes:

            id_cliente = cliente[0]

            nome = cliente[1]

            telefone = cliente[2]

            texto = (
                f"ID: {id_cliente}  |  "
                f"Nome: {nome}  |  "
                f"Telefone: {telefone}"
            )

            cliente_label = ctk.CTkLabel(
                self.pagina,
                text=texto,
                font=("Arial", 16)
            )

            cliente_label.pack(
                pady=5
            )


# ==========================================================
# INICIAR SISTEMA
# ==========================================================

if __name__ == "__main__":

    app = Sistema()

    app.mainloop()