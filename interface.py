
import customtkinter as ctk
import sqlite3
import os

from tkinter import messagebox
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

            # DASHBOARD
            if texto == "🏠 Dashboard":

                botao.configure(
                    command=self.abrir_dashboard
                )

            # CLIENTES
            elif texto == "👤 Clientes":

                botao.configure(
                    command=self.abrir_clientes
                )

            # ORÇAMENTOS
            elif texto == "📋 Orçamentos":

                botao.configure(
                    command=self.abrir_orcamentos
                )

            # RELATÓRIOS
            elif texto == "📄 Relatórios":

                botao.configure(
                    command=self.abrir_relatorios
                )

            # CONFIGURAÇÕES
            elif texto == "⚙ Configurações":

                botao.configure(
                    command=self.abrir_configuracoes
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

        if os.path.exists(caminho_logo):

            imagem_original = Image.open(
                caminho_logo
            )

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
        # TÍTULO
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
        # FRAME DAS PÁGINAS
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

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Bem-vindo ao OrçaSmart"
        )

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

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Cadastro de Clientes"
        )

        campo_nome = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Digite o nome do cliente",
            width=400,
            height=40
        )

        campo_nome.pack(
            pady=10
        )

        campo_telefone = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Digite o telefone",
            width=400,
            height=40
        )

        campo_telefone.pack(
            pady=10
        )

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

        if nome == "":

            messagebox.showwarning(
                "Atenção",
                "Digite o nome do cliente."
            )

            return

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT
            )
        """)

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

        conexao.commit()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Cliente cadastrado com sucesso!"
        )

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

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Clientes Cadastrados"
        )

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

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

        for cliente in clientes:

            id_cliente = cliente[0]
            nome = cliente[1]
            telefone = cliente[2] or "Não informado"

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

    # ======================================================
    # TELA DE ORÇAMENTOS
    # ======================================================

    def abrir_orcamentos(self):

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Gerenciamento de Orçamentos"
        )

        botao_novo = ctk.CTkButton(
            self.pagina,
            text="➕ Novo Orçamento",
            width=200,
            height=40,
            command=self.novo_orcamento
        )

        botao_novo.pack(
            pady=10
        )

        botao_listar = ctk.CTkButton(
            self.pagina,
            text="📋 Listar Orçamentos",
            width=200,
            height=40,
            command=self.listar_orcamentos_interface
        )

        botao_listar.pack(
            pady=10
        )

    # ======================================================
    # NOVO ORÇAMENTO
    # ======================================================

    def novo_orcamento(self):

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Novo Orçamento"
        )

        # BUSCAR CLIENTES

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome
            FROM clientes
            ORDER BY nome
        """)

        clientes = cursor.fetchall()

        conexao.close()

        # VERIFICAR CLIENTES

        if not clientes:

            mensagem = ctk.CTkLabel(
                self.pagina,
                text=(
                    "Nenhum cliente cadastrado.\n\n"
                    "Cadastre um cliente antes de criar um orçamento."
                ),
                font=("Arial", 18)
            )

            mensagem.pack(
                pady=50
            )

            return

        # CLIENTES

        label_cliente = ctk.CTkLabel(
            self.pagina,
            text="Cliente:"
        )

        label_cliente.pack(
            pady=(10, 2)
        )

        clientes_dict = {
            f"{cliente[0]} - {cliente[1]}": cliente[0]
            for cliente in clientes
        }

        combo_cliente = ctk.CTkComboBox(
            self.pagina,
            values=list(clientes_dict.keys()),
            width=400,
            height=40
        )

        combo_cliente.pack(
            pady=5
        )

        combo_cliente.set(
            list(clientes_dict.keys())[0]
        )

        # SERVIÇO

        label_servico = ctk.CTkLabel(
            self.pagina,
            text="Serviço:"
        )

        label_servico.pack(
            pady=(10, 2)
        )

        campo_servico = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Ex: Drywall, Forro de Gesso...",
            width=400,
            height=40
        )

        campo_servico.pack(
            pady=5
        )

        # ÁREA

        label_area = ctk.CTkLabel(
            self.pagina,
            text="Área (m²):"
        )

        label_area.pack(
            pady=(10, 2)
        )

        campo_area = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Ex: 20",
            width=400,
            height=40
        )

        campo_area.pack(
            pady=5
        )

        # VALOR M²

        label_valor = ctk.CTkLabel(
            self.pagina,
            text="Valor por m²:"
        )

        label_valor.pack(
            pady=(10, 2)
        )

        campo_valor_m2 = ctk.CTkEntry(
            self.pagina,
            placeholder_text="Ex: 120",
            width=400,
            height=40
        )

        campo_valor_m2.pack(
            pady=5
        )

        # VALOR TOTAL

        label_total = ctk.CTkLabel(
            self.pagina,
            text="Valor total: R$ 0,00",
            font=("Arial", 20, "bold")
        )

        label_total.pack(
            pady=15
        )

        # STATUS

        label_status = ctk.CTkLabel(
            self.pagina,
            text="Status:"
        )

        label_status.pack(
            pady=(5, 2)
        )

        combo_status = ctk.CTkComboBox(
            self.pagina,
            values=[
                "Pendente",
                "Aprovado",
                "Recusado"
            ],
            width=400,
            height=40
        )

        combo_status.pack(
            pady=5
        )

        combo_status.set(
            "Pendente"
        )

        # ==============================================
        # CALCULAR TOTAL
        # ==============================================

        def calcular_total(event=None):

            try:

                area = float(
                    campo_area.get().replace(",", ".")
                )

                valor_m2 = float(
                    campo_valor_m2.get().replace(",", ".")
                )

                total = area * valor_m2

                valor_formatado = (
                    f"R$ {total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                label_total.configure(
                    text=f"Valor total: {valor_formatado}"
                )

            except ValueError:

                label_total.configure(
                    text="Valor total: R$ 0,00"
                )

        campo_area.bind(
            "<KeyRelease>",
            calcular_total
        )

        campo_valor_m2.bind(
            "<KeyRelease>",
            calcular_total
        )

        # BOTÃO SALVAR

        botao_salvar = ctk.CTkButton(
            self.pagina,
            text="💾 Salvar Orçamento",
            width=250,
            height=45,
            command=lambda: self.salvar_orcamento_interface(
                clientes_dict,
                combo_cliente,
                campo_servico,
                campo_area,
                campo_valor_m2,
                combo_status
            )
        )

        botao_salvar.pack(
            pady=20
        )

    # ======================================================
    # SALVAR ORÇAMENTO
    # ======================================================

    def salvar_orcamento_interface(
        self,
        clientes_dict,
        combo_cliente,
        campo_servico,
        campo_area,
        campo_valor_m2,
        combo_status
    ):

        cliente_selecionado = combo_cliente.get()

        servico = campo_servico.get().strip()

        area_texto = campo_area.get().strip()

        valor_m2_texto = campo_valor_m2.get().strip()

        status = combo_status.get()

        # VALIDAÇÕES

        if not cliente_selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um cliente."
            )

            return

        if not servico:

            messagebox.showwarning(
                "Atenção",
                "Digite o serviço."
            )

            return

        try:

            area = float(
                area_texto.replace(",", ".")
            )

            valor_m2 = float(
                valor_m2_texto.replace(",", ".")
            )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite valores numéricos válidos."
            )

            return

        if area <= 0 or valor_m2 <= 0:

            messagebox.showwarning(
                "Atenção",
                "Área e valor do m² devem ser maiores que zero."
            )

            return

        cliente_id = clientes_dict[
            cliente_selecionado
        ]

        valor_total = area * valor_m2

        # SALVAR

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        # Garantir que a tabela existe

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orcamentos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                cliente_id INTEGER NOT NULL,

                servico TEXT NOT NULL,

                area REAL NOT NULL,

                valor_m2 REAL NOT NULL,

                valor_total REAL NOT NULL,

                status TEXT DEFAULT 'Pendente',

                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
            )
        """)

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
        conexao.close()

        valor_formatado = (
            f"R$ {valor_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        messagebox.showinfo(
            "Sucesso",
            (
                "Orçamento cadastrado com sucesso!\n\n"
                f"Valor total: {valor_formatado}"
            )
        )

        self.abrir_orcamentos()

    # ======================================================
    # LISTAR ORÇAMENTOS
    # ======================================================

    def listar_orcamentos_interface(self):

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Orçamentos Cadastrados"
        )

        conexao = sqlite3.connect(
            "orcamentos.db"
        )

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                orcamentos.id,
                clientes.nome,
                clientes.telefone,
                orcamentos.servico,
                orcamentos.area,
                orcamentos.valor_m2,
                orcamentos.valor_total,
                orcamentos.status,
                orcamentos.data_criacao

            FROM orcamentos

            INNER JOIN clientes
            ON orcamentos.cliente_id = clientes.id

            ORDER BY orcamentos.id DESC
        """)

        orcamentos = cursor.fetchall()

        conexao.close()

        # NENHUM ORÇAMENTO

        if not orcamentos:

            mensagem = ctk.CTkLabel(
                self.pagina,
                text="Nenhum orçamento cadastrado.",
                font=("Arial", 18)
            )

            mensagem.pack(
                pady=30
            )

            return

        # CONTAINER COM SCROLL

        frame_scroll = ctk.CTkScrollableFrame(
            self.pagina,
            width=800,
            height=400
        )

        frame_scroll.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # EXIBIR ORÇAMENTOS

        for orcamento in orcamentos:

            id_orcamento = orcamento[0]
            nome_cliente = orcamento[1]
            telefone = orcamento[2] or "Não informado"
            servico = orcamento[3]
            area = orcamento[4]
            valor_m2 = orcamento[5]
            valor_total = orcamento[6]
            status = orcamento[7]
            data = orcamento[8]

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
                f"Orçamento #{id_orcamento}\n"
                f"Cliente: {nome_cliente}\n"
                f"Telefone: {telefone}\n"
                f"Serviço: {servico}\n"
                f"Área: {area:.2f} m²\n"
                f"Valor por m²: {valor_m2_formatado}\n"
                f"Valor total: {valor_total_formatado}\n"
                f"Status: {status}\n"
                f"Data: {data}"
            )

            card = ctk.CTkFrame(
                frame_scroll,
                corner_radius=10
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            label = ctk.CTkLabel(
                card,
                text=texto,
                font=("Arial", 15),
                justify="left",
                anchor="w"
            )

            label.pack(
                padx=20,
                pady=15,
                anchor="w"
            )

    # ======================================================
    # RELATÓRIOS
    # ======================================================

    def abrir_relatorios(self):

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Relatórios"
        )

        mensagem = ctk.CTkLabel(
            self.pagina,
            text=(
                "Módulo de relatórios em desenvolvimento.\n\n"
                "Em breve você poderá gerar relatórios dos seus orçamentos."
            ),
            font=("Arial", 20)
        )

        mensagem.pack(
            pady=50
        )

    # ======================================================
    # CONFIGURAÇÕES
    # ======================================================

    def abrir_configuracoes(self):

        for widget in self.pagina.winfo_children():
            widget.destroy()

        self.titulo.configure(
            text="Configurações"
        )

        mensagem = ctk.CTkLabel(
            self.pagina,
            text=(
                "Configurações do sistema\n\n"
                "Módulo em desenvolvimento."
            ),
            font=("Arial", 20)
        )

        mensagem.pack(
            pady=50
        )


# ==========================================================
# INICIAR SISTEMA
# ==========================================================

if __name__ == "__main__":

    app = Sistema()

    app.mainloop()

