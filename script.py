import time
confirmacao = 'n'

while confirmacao == 'n':
    print('Coloque seus dados para terminar a compra:')
    name = input('coloque seu nome:')
    print('Processando...')
    time.sleep(1)
    CPF = input('Coloque seus Cpf:')
    print('Processando...')
    time.sleep(1)
    Telefone = input('Coloque seus numero de telefone:')
    print('Processando...')
    time.sleep(1)
    Aniversario = input('Coloque sua data de aniversario:')
    print('Processando...')
    time.sleep(1)
    print('Essas informações estão corretas?')
    print('nome', name, 'CPF', CPF, 'Telefone', Telefone, 'Data nascimento', Aniversario)

    confirmacao = input('Confirmar? (S/N): ').lower()

    if confirmacao == 's':
        print('Compra finalizada com sucesso!')
    elif confirmacao == 'n':
        print('Operação cancelada. Reincira os dados novamente.')
    else:
        print('Input invalido')