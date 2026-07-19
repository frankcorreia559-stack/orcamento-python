import tkinter as tk

def tela_cliente():
    
    janela_cliente = tk.Toplevel()
    janela.title('Sistema de Orçamentos')
    janela.geometry('400x300')

    tk.Label(janela_cliente, text="Nome do Cliente").pack()

    nome = tk.Entry(janela_cliente)
    nome.pack()

    tk.Label(janela_cliente, text='Telefone').pack()

    telefone = tk.Entry(janela_cliente)
    telefone.pack()

    def salvar():
        import sqlite3

        conexao = sqlite3.connect('orcamentos.db')
        cursor = conexao.cursor()

        cursor.execute("""
                       INSERT INTO clientes ( nome, telefone)
                       VALUES (?, ?)
                       """,
                       (nome.get(), telefone.get()))
        
        conexao.commit()
        conexao.close()

        nome.delete(0, tk.END)
        telefone.delete(0, tk.END)

        print('Cliente cadastrado!')

    botao = tk.Button(
        janela_cliente,
        text="Cadastrar",
        command=salvar
    )

    botao.pack(pady=20)

janela = tk.Tk()

janela.title("Sistema de Orçamentos")
janela.geometry("500x400")


titulo = tk.Label(
    janela,
    text="SISTEMA DE ORÇAMENTOS",
    font=("Arial", 16)
)

titulo.pack(pady=30)


botao_cliente = tk.Button(
    janela,
    text="Cadastrar Cliente",
    command=tela_cliente
)

botao_cliente.pack()


janela.mainloop()

