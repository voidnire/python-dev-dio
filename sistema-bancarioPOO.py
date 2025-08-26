from abc import abstractclassmethod, abstractproperty
from datetime import datetime, timedelta
import textwrap
import pytz


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco 
        self.contas = []

    def realizar_transa(self,conta,transa):
        transa.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

    

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self.transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero # unique
        self._cliente = cliente 
        self._saldo = 0
        self._agencia ="0001"
        self._historico = Historico() #classe

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):  
        return self._agencia

    @property
    def cliente(self):  
        return self._cliente
    
    @property
    def historico(self):  
        return self._historico

    
    def sacar(self,valor):  
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não possui saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido.")

        return 
        
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido.")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero,cliente,limite=500,limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques 
    
    def sacar(self,valor):
        numero_saques = len([transa for transa in self.historico.transacoes
                             if transa["tipo"] == "Saque"])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t{self.numero}
        Titular:\t{self.cliente.nome}
        """


def criar_cliente(clientes):
    cpf = input("Informe o CPF (apenas números): ")
    if cpf in [c.cpf for c in clientes]:
        print("CPF já cadastrado.")
        return None

    nome = input("Informe o nome do cliente: ")
    data_nasc = input("Informe a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Informe o endereço: ")

    


    cliente = PessoaFisica(nome=nome,data_nascimento=data_nasc,cpf=cpf,endereco=endereco)

    clientes.append(cliente)
    

    print("\n Cliente criado com sucesso.")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return None
    
    if len(cliente.contas) > 1:
        print("Cliente possui mais de uma conta.")
        for i, conta in enumerate(cliente.contas):
            print(f"[{i}] - {conta}")
        idx = int(input("Selecione a conta desejada: "))
        return cliente.contas[idx]
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transa = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transa(conta, transa)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transa = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transa(conta, transa)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transa in transacoes:
            extrato += f"{transa['data']} - {transa['tipo']}: R$ {transa['valor']:.2f}\n"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=========================================")

def criar_conta(numero, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado.")
        return

    conta = ContaCorrente.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("======================================================="
        )
        print(textwrap.dedent(str(conta)))

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def listar_contas():
    pass

def main():    
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(
                "\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@"
            )


main()

