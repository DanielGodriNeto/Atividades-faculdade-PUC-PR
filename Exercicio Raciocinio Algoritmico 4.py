#Imprima os numeros de 1 a 10 de forma crescente e decrescente
#Solicite valor de 1 a 10 e imprima tabuada desse numero

while True:
    try:
        numero = float(input("Digite um número de 1 a 10: "))
        break
    except ValueError:
        print("Entrada inválida. Digite um número.")

if numero < 1 or numero > 10:
    print("Número inválido. Por favor, digite um número de 1 a 10.")
else:
    print("\nNúmeros de 1 a 10 em ordem crescente:")
    for i in range(1, 11):
        print(i)

    print("\nNúmeros de 10 a 1 em ordem decrescente:")
    for i in range(10, 0, -1):
        print(i)

    print(f"\nTabuada do {numero}:")
    for i in range(1, 11):
        print(f"{numero} x {i} = {numero * i}")   

#Peca ao usuario uma palavra de no minimo 3 letras e no maximo 10 letras
#E imprima a palavra digitada e o numero de letras

palavra = input("Digite uma palavra de no mínimo 3 letras e no máximo 10 letras: ")
if len(palavra) < 3 or len(palavra) > 10:
    print("Palavra inválida. Por favor, digite uma palavra de no mínimo 3 letras e no máximo 10 letras.")
else:
    print(f"Palavra digitada: {palavra}")
    print(f"Número de letras: {len(palavra)}")

#Peca ao usuario sua nota (0-10) e verifique se e valida
#Se for invalido repita a pergunta ate que seja valido

while True:
    try:
        nota = float(input("Digite sua nota (0-10): "))
        if 0 <= nota <= 10:
            print(f"Nota válida: {nota}")
            break
        else:
            print("Nota inválida. Por favor, digite uma nota entre 0 e 10.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

#Implemente um programa em Python para imprimir na tela o
#somatório dos N primeiros números inteiros a partir do 1. Sendo N
#lido do teclado

while True:
    try:
        N = int(input("Digite o valor de N: "))
        break
    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")

somatorio = 0

for i in range(1, N + 1):
    somatorio += i

print(f"O somatório dos {N} primeiros números inteiros a partir do 1 é: {somatorio}")

#Implemente um programa em Python para ler do teclado números.
#Caso o usuário forneça um número igual a -1, o programa deve
#fornecer a média dos números e encerrar

numeros = []
while True:
    try:
        n = float(input("Digite um número (ou -1 para encerrar): "))
        if n == -1:
            break
        numeros.append(n)
    except ValueError:
        print("Entrada inválida. Digite um número válido.")

if numeros:
    media = sum(numeros) / len(numeros)
    print(f"A média dos números digitados é: {media}")
else:
    print("Nenhum número foi digitado.")

# Escreva um programa que receba 10 números do teclado
# exiba aquantidade de números pares e ímpares lidos.

pares = 0
impares = 0

for i in range(10):
    while True:
        try:
            numero = int(input("Digite um número: "))
            break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
    if numero % 2 == 0:
        pares += 1
    else:
        impares += 1
print(f"Quantidade de números pares: {pares}")
print(f"Quantidade de números ímpares: {impares}")


# Calculdadora PEMDAS Desafio 
#Nível 4: Muito Difícil

# O programa deve aceitar uma expressão completa, incluindo:

# vários números
# vários operadores
# uso de parênteses
# Exemplos:

# 2 * (3 + 5 - 1)
# (10 - 2) * 3
# 8 + 2 * (4 - 1)
# Nesta versão, o programa deve resolver corretamente a expressão considerando:

# os parênteses
# a prioridade entre operadores

def calcular_expressao(expressao):
    try:
        resultado = eval(expressao)
        return resultado
    except Exception as e:
        return f"Erro ao calcular a expressão: {e}"
expressao = input("Digite uma expressão matemática: ")
resultado = calcular_expressao(expressao) 
print(f"O resultado da expressão '{expressao}' é: {resultado}")
