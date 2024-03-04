from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class MsgHandler:
    log = ""

    @classmethod
    def print_error(cls, op, msg):
        txt = f"### {op} - Erro: {msg} ###\n"
        print(txt)
        cls.log += txt

    @classmethod
    def print_fail(cls, op, msg):
        txt = f"@@@ {op} - Falha: {msg} @@@\n"
        print(txt)
        cls.log += txt
    
    @classmethod
    def print_success(cls, op, msg):
        txt = f"=== {op} - Sucesso: {msg} ===\n"
        print(txt)
        cls.log += txt
    
    @classmethod
    def show_log(cls):
        print(cls.log)

class Cliente:
    def __init__(self, endereco) -> None:
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, nascimento) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = nascimento

class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            MsgHandler.print_fail("Sacar", "Saldo insuficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            MsgHandler.print_success("Sacar", "Saque realizado.")
            return True
        
        else:
            MsgHandler.print_fail("Sacar", "Valor inválido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            MsgHandler.print_success("Depositar", "Depósito realizado.")
            return True
        
        else:
            MsgHandler.print_fail("Depositar", "Valor inválido.")
        
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            MsgHandler.print_fail("Sacar", f"Excedeu o valor limite {self._limite}.")
        
        elif excedeu_saques:
            MsgHandler.print_fail("Sacar", f"Excedeu número máximo de saques {self._limite_saques}")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente._nome}
        """

class Historico:
    def __init__(self) -> None:
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor) -> None:
        super().__init__()
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor) -> None:
        super().__init__()
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    prompt = '''
    ===== SELECIONE =====
    [ d]\tDepositar
    [ s]\tSacar
    [ e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [ l]\t Log
    [ q]\tSair

    '''
    return input(prompt)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        MsgHandler.print_fail("Sacar", "Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        MsgHandler.print_fail("Depositar", "Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        MsgHandler.print_fail("Extrato", "Cliente não encontrado!")
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
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        MsgHandler.print_fail("Recuperar Conta", "Cliente não possui conta.")
        return
    
    return cliente._contas[0]

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        MsgHandler.print_fail("Criar Cliente", "CPF já em uso.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome=nome, nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    MsgHandler.print_success("Criar Cliente", "Cliente criado.")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        MsgHandler.print_fail("Criar Conta", "Cliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    MsgHandler.print_success("Criar Conta", "Conta criada.")

def listar_contas(contas):
    for conta in contas:
        print(conta)

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

        elif opcao == "l":
            MsgHandler.show_log()

        else:
            MsgHandler.print_fail("Main", "Seleção inválida.")

if __name__ == "__main__":
    main()
