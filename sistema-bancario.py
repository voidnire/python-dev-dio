from datetime import datetime, timedelta
import pytz

menu = """

[d] depositar
[s] sacar
[e] extrato
[q] quit

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITES = 3


while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("ERRO: O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor a sacar: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITES

        if excedeu_saldo:
            print("ERRO: Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("ERRO: O valor do saque excede o limite.")

        elif excedeu_saques:
            print("ERRO: Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Ainda foram realizadas movimentações." if not extrato else extrato)
        print(f"\SALDO: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("ERRO: Operação inválida. Selecione a operação desejada.")
