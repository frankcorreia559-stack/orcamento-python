import customtkinter as ctk

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

class Sistema(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fs ART Gesso & Drywall")
        self.geometry('1200x700')
        self.minsize(1000, 600)

        # menu lateral

        self.menu = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu.pack(side='left', fill='y')

        self.logo =ctk.CTkLabel(
            self.menu,
            text='Fs ART\nGesso & Drywall',
            font=('Arial', 22, 'bold')
        )
        self.logo.pack(pady=30)

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
                height=40
            )

            botao.pack(pady=8)

        # Área principal
        self.conteudo = ctk.CTkFrame(self)
        self.conteudo.pack(side="right", fill="both", expand=True)

        titulo = ctk.CTkLabel(
            self.conteudo,
            text="Bem-vindo ao Sistema de Orçamentos",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=40)





    


