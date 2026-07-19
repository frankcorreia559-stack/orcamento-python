from cadastrar_cliente import cadastrar_cliente
from listar_clientes import listar_clientes
from editar_cliente import editar_cliente
from cadastrar_orcamento import cadastrar_orcamento
from listar_orcamentos import listar_orcamentos
from excluir_cliente import excluir_cliente


while True:
    print("\n===== SISTEMA DE ORÇAMENTOS =====")
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Editar Cliente")
    print("4 - Cadastrar Orçamento")
    print("5 - Listar Orçamentos")
    print("6 - Excluir cliente")
    print("7 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_cliente()

    elif opcao == "2":
        listar_clientes()

    elif opcao == "3":
        editar_cliente()    

    elif opcao == "4":
        cadastrar_orcamento()

    elif opcao == "5":
        listar_orcamentos()

    elif opcao == "6":
        excluir_cliente()

    elif opcao == "7":
        print("Sistema encerrado.") 
        break

    else:
        print("Opção inválida!")