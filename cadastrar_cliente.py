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

    try:

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

        sucesso = True
        mensagem = "Cliente cadastrado com sucesso!"

    except sqlite3.Error as erro:

        sucesso = False
        mensagem = f"Erro ao cadastrar cliente:\n{erro}"

    # ==============================================
    # TRATAMENTO DO RESULTADO
    # ==============================================

    if sucesso:

        messagebox.showinfo(
            "Sucesso",
            mensagem
        )

        campo_nome.delete(
            0,
            "end"
        )

        campo_telefone.delete(
            0,
            "end"
        )

        campo_nome.focus()

    else:

        messagebox.showwarning(
            "Atenção",
            mensagem
        )