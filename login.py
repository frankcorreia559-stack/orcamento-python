import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

from usuarios import (
    criar_tabela_usuarios,
    criar_conta,
    autenticar_usuario
)

from banco import criar_tabelas


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==========================================================
# TELA DE LOGIN
# ==========================================================

class Login(ctk.CTk):

    def __init__(self):

        super().__init__()

        # --------------------------------------------------
        # INICIALIZAR BANCO
        # --------------------------------------------------

        criar_tabelas()
        criar_tabela_usuarios()

        # --------------------------------------------------
        # CONFIGURAÇÃO DA JANELA
        # --------------------------------------------------

        self.title(
            "OrçaSmart - Login"
        )

        self.geometry(
            "500x600"
        )

        self.resizable(
            False,
            False
        )

        # --------------------------------------------------
        # CENTRALIZAR JANELA
        # --------------------------------------------------

        self.update_idletasks()

        largura = 500
        altura = 600

        x = (
            self.winfo_screenwidth()
            - largura
        ) // 2

        y = (
            self.winfo_screenheight()
            - altura
        ) // 2

        self.geometry(
            f"{largura}x{altura}+{x}+{y}"
        )

        # --------------------------------------------------
        # FUNDO DA JANELA
        # --------------------------------------------------

        self.configure(
            fg_color="#181818"
        )

        # --------------------------------------------------
        # CONTAINER PRINCIPAL
        # --------------------------------------------------

        self.frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#242424"
        )

        self.frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        caminho_logo = os.path.join(
            os.path.dirname(__file__),
            "logo_orcamento.png"
        )

        if os.path.exists(caminho_logo):

            try:

                imagem_logo = Image.open(
                    caminho_logo
                )

                self.logo = ctk.CTkImage(
                    light_image=imagem_logo,
                    dark_image=imagem_logo,
                    size=(280, 150)
                )

                ctk.CTkLabel(
                    self.frame,
                    text="",
                    image=self.logo
                ).pack(
                    pady=(20, 0)
                )

            except Exception:

                ctk.CTkLabel(
                    self.frame,
                    text="OrçaSmart",
                    font=ctk.CTkFont(
                        size=32,
                        weight="bold"
                    )
                ).pack(
                    pady=(25, 5)
                )

        else:

            ctk.CTkLabel(
                self.frame,
                text="OrçaSmart",
                font=ctk.CTkFont(
                    size=32,
                    weight="bold"
                )
            ).pack(
                pady=(25, 5)
            )

        # --------------------------------------------------
        # SUBTÍTULO
        # --------------------------------------------------

        ctk.CTkLabel(
            self.frame,
            text="Sistema de Orçamentos",
            text_color="#BDBDBD",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            pady=(0, 20)
        )

        # --------------------------------------------------
        # USUÁRIO
        # --------------------------------------------------

        self.entry_usuario = ctk.CTkEntry(
            self.frame,
            width=350,
            height=45,
            placeholder_text="Usuário",
            fg_color="#303030",
            border_color="#555555"
        )

        self.entry_usuario.pack(
            pady=8
        )

        # --------------------------------------------------
        # SENHA
        # --------------------------------------------------

        self.entry_senha = ctk.CTkEntry(
            self.frame,
            width=350,
            height=45,
            placeholder_text="Senha",
            show="*",
            fg_color="#303030",
            border_color="#555555"
        )

        self.entry_senha.pack(
            pady=8
        )

        # --------------------------------------------------
        # BOTÃO ENTRAR
        # --------------------------------------------------

        ctk.CTkButton(
            self.frame,
            text="ENTRAR",
            width=350,
            height=45,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.fazer_login
        ).pack(
            pady=(18, 8)
        )

        # --------------------------------------------------
        # BOTÃO CRIAR CONTA
        # --------------------------------------------------

        ctk.CTkButton(
            self.frame,
            text="Criar nova conta",
            width=350,
            height=40,
            fg_color="transparent",
            border_width=1,
            border_color="#4A90E2",
            text_color="#6EA8E8",
            hover_color="#303030",
            command=self.abrir_criar_conta
        ).pack(
            pady=8
        )

        # --------------------------------------------------
        # VERSÃO
        # --------------------------------------------------

        ctk.CTkLabel(
            self.frame,
            text="OrçaSmart - Versão 1.0",
            text_color="#777777",
            font=ctk.CTkFont(
                size=10
            )
        ).pack(
            side="bottom",
            pady=15
        )

        # --------------------------------------------------
        # ENTER PARA LOGIN
        # --------------------------------------------------

        self.bind(
            "<Return>",
            lambda evento: self.fazer_login()
        )

        self.entry_usuario.focus()


    # ======================================================
    # FAZER LOGIN
    # ======================================================

    def fazer_login(self):

        usuario = (
            self.entry_usuario
            .get()
            .strip()
        )

        senha = (
            self.entry_senha
            .get()
            .strip()
        )

        if not usuario:

            messagebox.showwarning(
                "Atenção",
                "Digite o usuário."
            )

            self.entry_usuario.focus()

            return

        if not senha:

            messagebox.showwarning(
                "Atenção",
                "Digite a senha."
            )

            self.entry_senha.focus()

            return

        sucesso, dados_usuario = (
            autenticar_usuario(
                usuario,
                senha
            )
        )

        if sucesso:

            self.abrir_sistema(
                dados_usuario
            )

        else:

            messagebox.showerror(
                "Login inválido",
                "Usuário ou senha incorretos."
            )

            self.entry_senha.delete(
                0,
                "end"
            )

            self.entry_senha.focus()


    # ======================================================
    # ABRIR SISTEMA
    # ======================================================

    def abrir_sistema(
        self,
        usuario
    ):

        self.destroy()

        from interface import Sistema

        app = Sistema(
            usuario_logado=usuario
        )

        app.mainloop()


    # ======================================================
    # CRIAR CONTA
    # ======================================================

    def abrir_criar_conta(self):

        janela = ctk.CTkToplevel(
            self
        )

        janela.title(
            "Criar Conta"
        )

        janela.geometry(
            "500x550"
        )

        janela.resizable(
            False,
            False
        )

        janela.configure(
            fg_color="#181818"
        )

        janela.grab_set()

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        ctk.CTkLabel(
            janela,
            text="Criar Conta",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=(40, 10)
        )

        ctk.CTkLabel(
            janela,
            text="Cadastre seu acesso ao OrçaSmart",
            text_color="#BDBDBD",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            pady=(0, 30)
        )

        # --------------------------------------------------
        # NOME
        # --------------------------------------------------

        entry_nome = ctk.CTkEntry(
            janela,
            width=380,
            height=45,
            placeholder_text="Nome completo",
            fg_color="#303030",
            border_color="#555555"
        )

        entry_nome.pack(
            pady=10
        )

        # --------------------------------------------------
        # USUÁRIO
        # --------------------------------------------------

        entry_usuario = ctk.CTkEntry(
            janela,
            width=380,
            height=45,
            placeholder_text="Nome de usuário",
            fg_color="#303030",
            border_color="#555555"
        )

        entry_usuario.pack(
            pady=10
        )

        # --------------------------------------------------
        # SENHA
        # --------------------------------------------------

        entry_senha = ctk.CTkEntry(
            janela,
            width=380,
            height=45,
            placeholder_text="Senha",
            show="*",
            fg_color="#303030",
            border_color="#555555"
        )

        entry_senha.pack(
            pady=10
        )

        # --------------------------------------------------
        # CONFIRMAR SENHA
        # --------------------------------------------------

        entry_confirmar = ctk.CTkEntry(
            janela,
            width=380,
            height=45,
            placeholder_text="Confirmar senha",
            show="*",
            fg_color="#303030",
            border_color="#555555"
        )

        entry_confirmar.pack(
            pady=10
        )

        # --------------------------------------------------
        # SALVAR CONTA
        # --------------------------------------------------

        def salvar_conta():

            nome = (
                entry_nome
                .get()
                .strip()
            )

            usuario = (
                entry_usuario
                .get()
                .strip()
            )

            senha = (
                entry_senha
                .get()
                .strip()
            )

            confirmar = (
                entry_confirmar
                .get()
                .strip()
            )

            if not nome:

                messagebox.showwarning(
                    "Atenção",
                    "Digite seu nome completo.",
                    parent=janela
                )

                return

            if not usuario:

                messagebox.showwarning(
                    "Atenção",
                    "Digite um nome de usuário.",
                    parent=janela
                )

                return

            if not senha:

                messagebox.showwarning(
                    "Atenção",
                    "Digite uma senha.",
                    parent=janela
                )

                return

            if senha != confirmar:

                messagebox.showerror(
                    "Erro",
                    "As senhas não são iguais.",
                    parent=janela
                )

                return

            sucesso, mensagem = (
                criar_conta(
                    nome,
                    usuario,
                    senha
                )
            )

            if sucesso:

                messagebox.showinfo(
                    "Conta criada",
                    mensagem,
                    parent=janela
                )

                janela.destroy()

                self.entry_usuario.delete(
                    0,
                    "end"
                )

                self.entry_senha.delete(
                    0,
                    "end"
                )

                self.entry_usuario.insert(
                    0,
                    usuario
                )

                self.entry_senha.focus()

            else:

                messagebox.showerror(
                    "Erro",
                    mensagem,
                    parent=janela
                )

        # --------------------------------------------------
        # BOTÃO CRIAR CONTA
        # --------------------------------------------------

        ctk.CTkButton(
            janela,
            text="Criar Conta",
            width=250,
            height=45,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=salvar_conta
        ).pack(
            pady=30
        )


# ==========================================================
# EXECUTAR LOGIN
# ==========================================================

if __name__ == "__main__":

    app = Login()

    app.mainloop()