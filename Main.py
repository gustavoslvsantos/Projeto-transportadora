import sqlite3
import time
import sys
from time import sleep
from tabulate import tabulate
from pyfiglet import Figlet

conn = sqlite3.connect("pedidos.db")
db_cursor = conn.cursor()

db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS entregas (
                codigo_pedido INTEGER NOT NULL PRIMARY KEY,
                nota_fiscal INTEGER NOT NULL,
                numero_frete INTEGER NOT NULL,
                valor_frete DOUBLE NOT NULL,
                nome_cliente TEXT NOT NULL,
                destinatario TEXT NOT NULL,
                endereco_origem TEXT NOT NULL,
                endereco_destino TEXT NOT NULL,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                motorista TEXT NOT NULL,
                placa TEXT NOT NULL,
                rota TEXT NOT NULL
                );
                """)

def extTxt(txt):
    for char in txt:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0)

def inserir_pedido():
    try:
        u_codigo_pedido = int(input("Digite o codigo do pedido: "))
        u_nota_fiscal = int(input("Digite a nota fiscal: "))
        u_numero_frete = int(input("Digite o numero do frete: "))
        u_valor_frete = float(input("Digite o valor do frete: "))
        u_nome_cliente = input("Digite o nome do cliente: ")
        u_destinatario = input("Digite o destinatario: ")
        u_endereco_origem = input("Digite o endereço de origem: ")
        u_endereco_destino = input("Digite o endereço de destino: ")
        u_produto = input("Digite o nome do produto: ")
        u_quantidade = int(input("Digite a quantidade do produto: "))
        u_motorista = input("Digite o nome do motorista responsavel: ")
        u_placa = input("Digite a placa do caminhao: ")
        u_rota = input("Digite a rota que ser utilizada: ")
    
        db_cursor.execute(
            f"""INSERT INTO entregas(codigo_pedido, nota_fiscal, numero_frete, valor_frete, nome_cliente, destinatario, endereco_origem, endereco_destino, produto, quantidade, motorista, placa, rota) 
            VALUES ({u_codigo_pedido},{u_nota_fiscal},{u_numero_frete},{u_valor_frete},'{u_nome_cliente}','{u_destinatario}','{u_endereco_origem}','{u_endereco_destino}','{u_produto}',{u_quantidade},'{u_motorista}','{u_placa}','{u_rota}')""")
    except Exception as e:
        extTxt('\nErro ao inserir o pedido\n')
        extTxt(f'Cancelando operação: {e}\n')
    else:
        conn.commit()
        extTxt("\nInserido com sucesso!\n")


def imprimir_elegante():
        db_cursor.execute('SELECT * FROM entregas')
        result = db_cursor.fetchall()
        print(tabulate(result, headers=['Codigo', 'Nota fiscal', 'Numero frete', 'Valor frete', 'Nome Cliente',
                                    'Destinarario', 'End. Origem', 'End. Destino', 'Produto', 'Quantidade', 'Motorista', 'Placa', 'Rota'], tablefmt='fancy_grid'))



def atualizar_pedido(codigo_pedido, novo_endereco_destino, novo_motorista, nova_placa, nova_rota, novo_frete):
    try:
        db_cursor.execute(
            f"""UPDATE entregas SET endereco_destino=?, motorista=?, placa=?, rota=?, valor_frete=? WHERE codigo_pedido=?""",(novo_endereco_destino, novo_motorista, nova_placa, nova_rota, novo_frete, codigo_pedido))
    except Exception as e:
        extTxt('\nErro ao atualizar o pedido\n')
        extTxt(f'Cancelando operação: {e}\n')
    else:
        conn.commit()
        extTxt("\nAtualizado com sucesso!\n")


def deletar_pedido(codigo_pedido):
    try:
        db_cursor.execute(
        f"DELETE FROM entregas WHERE codigo_pedido = {codigo_pedido}")
    except Exception as e:
        extTxt('\nErro ao deletar o pedido\n')
        extTxt(f'Cancelando operação: {e}\n')
    else:
        conn.commit()
        extTxt("\nDeletado com sucesso!\n")


while True:
    result = Figlet(font='doom')
    extTxt(result.renderText('Transportadora'))
    print ("""\n
 ########################################
 #######   REGISTROS DE ENTREGAS  #######
 ########################################
          \n""")
    print (tabulate([['# 1 ->', '    Adicionar novo pedido'], ['# 2 ->', '   Imprimir pedidos'], ['# 3 ->', '    Atualizar pedido'], ['# 4 ->', '    Deletar pedido'], ['# 0 ->', '    Sair']],
                   headers=['   # Número: ','   # Função: '], tablefmt='fancy_grid'))
   
    try:
        opcao = int(input("\nDigite o número da função desejada: \n"))
        if opcao == 0:
            break
        if opcao == 1:
            inserir_pedido()
        if opcao == 2:
            imprimir_elegante()
        if opcao == 3:
            codigo_pedido = int(input("Digite o codigo do pedido: \n"))
            novo_endereco_destino = input("Digite o novo endereço de destino: \n")
            novo_motorista = input("Digite o nome do motorista responsavel: \n")
            nova_placa = input("Digite a placa do caminhao: \n")
            nova_rota = input("Digite a rota que ser utilizada: \n")
            novo_frete = input("Digite o valor do frete: \n")
            atualizar_pedido(codigo_pedido, novo_endereco_destino,
                             novo_motorista, nova_placa, nova_rota, novo_frete)
        if opcao == 4:
            codigo_pedido = int(
                input("Digite o codigo do pedido a ser deletado:  \n"))
            deletar_pedido(codigo_pedido)
    except ValueError:  
        print('Digite um número válido!')

conn.commit()
conn.close()
print('Fim')
