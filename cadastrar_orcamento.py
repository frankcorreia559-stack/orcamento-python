import sqlite3

def cadastrar_orcamento():
    
    conexao = sqlite3.connect('orcamentos.db')
    cursor = conexao.cursor()

    print('\n======= NOVO ORCAMENTO ========')

    cliente_id = int(input('ID do cliente: '))
    servico = input('serviço: ')
    area = float(input('Área em m²: '))
    valor_m2 = float(input('VAlor do m²: '))

    valor_total = area * valor_m2

    cursor.execute("""
                  INSERT INTO orcamentos
                  (cliente_id, servico, area, valor_m2, valor_total)
                  VALUES (?, ?, ?, ?, ?)
                  """,(cliente_id, servico, area, valor_m2, valor_total))

    conexao.commit()
    conexao.close()

    print(f'\nOrçamento cadastrado!')
    print(f'Valor total: R$ {valor_total:.2f}')