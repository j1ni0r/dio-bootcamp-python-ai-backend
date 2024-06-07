import os
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.registrar(conta)
 
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
        self.cliente.adicionar_conta(self)

    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Transacao(valor, "Depósito"))
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
        return True

    def sacar(self, valor):
        raise NotImplementedError("Método sacar deve ser implementado pela classe filha")

class ContaCorrente(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self.limite = 500
        self.limite_saques = 3

    def sacar(self, valor):
        if valor > 0:
            if self.saldo >= valor:
                if len([transacao for transacao in self.historico.transacoes if transacao.descricao == 'Saque' and transacao.data.date() == datetime.today().date()]) < self.limite_saques:
                    self.saldo -= valor
                    self.historico.adicionar_transacao(Transacao(valor, "Saque"))
                    print("Saque realizado com sucesso!")
                    return True
                else:
                    print("Operação falhou! Número máximo de saques excedido.")
            else:
                print("Operação falhou! Você não tem saldo suficiente.")
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def __init__(self, valor, descricao):
        self.valor = valor
        self.descricao = descricao
        self.data = datetime.now()

    def registrar(self, conta):
        print(f"Transação {self.descricao} de R$ {self.valor:.2f} realizada com sucesso na conta {conta.numero}.")

def menu():
    """Exibe o menu de opções para o usuário."""
    menu = """
BEM VINDO AO BANCO SIMPLES V.0.03 [Com POO]

Escolha uma opção:
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """
    return input(menu)

def depositar(conta):
    """Realiza o depósito na conta."""
    valor = float(input("Informe o valor do depósito: "))
    conta.depositar(valor)

def sacar(conta):
    """Realiza o saque da conta."""
    valor = float(input("Informe o valor do saque: "))
    conta.sacar(valor)

def exibir_extrato(conta):
    """Exibe o extrato da conta."""
    os.system('cls')
    print("\n================ EXTRATO ================")
    if conta.historico.transacoes:
        for transacao in conta.historico.transacoes:
            print(f"{transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao.descricao}: R$ {transacao.valor:.2f}")
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def filtrar_usuario(usuarios, cpf):
    """Filtra a lista de usuários buscando o CPF informado."""
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_usuario(usuarios):
    """Cria um novo usuário."""
    os.system('cls')
    cpf = input("Informe o CPF do usuário (somente números): ")
    if filtrar_usuario(usuarios, cpf) is not None:
        print("Usuário já cadastrado!")
    else:
        nome = input("Informe o nome do usuário: ")
        while True:
            data_nascimento = input("Informe a data de nascimento do usuário (AAAA-MM-DD): ")
            try:
                data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Data inválida! Por favor, utilize o formato AAAA-MM-DD.")
        endereco = input("Informe o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")  # Solicita o endereço
        usuario = PessoaFisica(endereco, cpf, nome, data_nascimento)  # Cria a instância de PessoaFisica
        usuarios.append(usuario)
        print("Usuário criado com sucesso!")
    return usuarios


def criar_conta(clientes, contas):
    """Cria uma nova conta para o usuário."""
    os.system('cls')
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(clientes, cpf)

    if usuario:
        numero_conta = len(contas) + 1
        conta = ContaCorrente(usuario, numero_conta)
        contas.append(conta)
        print(f"Conta criada com sucesso! \nAgência: {conta.agencia} \nNúmero da conta: {conta.numero}")
    else:
        print("Usuário não encontrado!")

def listar_contas(contas):
    """Lista as contas cadastradas."""
    os.system('cls')
    if contas:
        print("\n================ Contas Cadastradas ================")
        for conta in contas:
            print(f"Agência: {conta.agencia} | Número da conta: {conta.numero} | Usuário: {conta.cliente.nome}")
        print("====================================================")
    else:
        print("Nenhuma conta cadastrada.")

def main():
    """Função principal do sistema bancário."""
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(clientes, cpf)
            if usuario:
                for conta in usuario.contas:
                    print(f"Conta número: {conta.numero}")
                numero_conta = int(input("Informe o número da conta para depósito: "))
                for conta in usuario.contas:
                    if conta.numero == numero_conta:
                        depositar(conta)
                        break
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "s":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(clientes, cpf)
            if usuario:
                for conta in usuario.contas:
                    print(f"Conta número: {conta.numero}")
                numero_conta = int(input("Informe o número da conta para saque: "))
                for conta in usuario.contas:
                    if conta.numero == numero_conta:
                        sacar(conta)
                        break
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "e":
            cpf = input("Informe o CPF do titular da conta: ")
            usuario = filtrar_usuario(clientes, cpf)
            if usuario:
                for conta in usuario.contas:
                    print(f"Conta número: {conta.numero}")
                numero_conta = int(input("Informe o número da conta para exibir o extrato: "))
                for conta in usuario.contas:
                    if conta.numero == numero_conta:
                        exibir_extrato(conta)
                        break
                else:
                    print("Conta não encontrada.")
            else:
                print("Usuário não encontrado.")
        elif opcao == "nu":
            clientes = criar_usuario(clientes)
        elif opcao == "nc":
            criar_conta(clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()