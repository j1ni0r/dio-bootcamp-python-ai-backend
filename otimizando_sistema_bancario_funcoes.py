import os
def menu():
    """Exibe o menu de opções para o usuário."""
    menu = """
BEM VINDO AO BANCO SIMPLES V.0.02 [Com Funções]

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

def depositar(saldo, valor, extrato, /):
    """Realiza o depósito e atualiza o saldo e extrato."""
    # os.system('cls')
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!\n")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza o saque e atualiza o saldo, extrato e número de saques."""
    # os.system('cls')
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!\n")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """Exibe o extrato das operações realizadas."""
    os.system('cls')
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def filtrar_usuario(usuarios, cpf):
    """Filtra a lista de usuários buscando o CPF informado."""
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
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
        data_nascimento = input("Informe a data de nascimento do usuário (AAAA-MM-DD): ")
        endereco = input("Informe o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")
        usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
        usuarios.append(usuario)
        print("Usuário criado com sucesso!")
    return usuarios
### 
""" O Código abaixo está comentado pois eu resolvi adaptar a ideia da resolução do professor
Na minha versão, a validação do CPF só ocorria no final depois de ter preenchido
todos os dados. O código novo agora pega a ideia de validar cpf logo que é digitado!
"""
# def criar_usuario(usuarios):
#     """Cria um novo usuário."""
#     nome = input("Informe o nome do usuário: ")
#     data_nascimento = input("Informe a data de nascimento do usuário (AAAA-MM-DD): ")
#     cpf = input("Informe o CPF do usuário (somente números): ")
#     endereco = input("Informe o endereço do usuário (logradouro, nro - bairro - cidade/sigla estado): ")

#     usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

#     if filtrar_usuario(usuarios, cpf) is None:
#         usuarios.append(usuario)
#         print("Usuário criado com sucesso!")
#     else:
#         print("Usuário já cadastrado!")

#     return usuarios
def saldo_atual(saldo):
    print((f"\nSaldo Atual: R$ [{saldo:.2f}]"))


def criar_conta(agencia, numero_conta, usuarios):
    """Cria uma nova conta para o usuário."""
    os.system('cls')
    cpf = input("Informe o CPF do usuário: ")

    usuario = filtrar_usuario(usuarios, cpf)

    if usuario:
        print(f"Conta criada com sucesso! \nAgência: {agencia} \nNúmero da conta: {numero_conta}")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    else:
        print("Usuário não encontrado!")
        return None

def listar_contas(contas):
    os.system('cls')
    """Lista as contas cadastradas."""
    if contas:
        print("\n================ Contas Cadastradas ================")
        for conta in contas:
            print(f"Agência: {conta['agencia']} | Número da conta: {conta['numero_conta']} | Usuário: {conta['usuario']['nome']}")
        print("====================================================")
    else:
        print("Nenhuma conta cadastrada.")

def main():
    """Função principal do sistema bancário."""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
            # os.system('cls')
            saldo_atual(saldo)


        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            saldo_atual(saldo)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            usuarios = criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            os.system('cls')
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
