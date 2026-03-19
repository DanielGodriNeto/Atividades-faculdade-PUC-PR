import time

print ('Hello World')

# Exercicio 1
# Verificar se a pessoa e de maior ou menor idade
# Se a idade for maior ou igual a 18 anos e de maior
# Se a idade for menor ou igual a 17 anos e de menor

time.sleep(1)
idade = float(input('Qual sua idade: '))
if (idade > 17):
    print ('Voce e de maior')
else:
    print ('Voce e de menor')


#Exercicio 2
# Verificar a temperatura ambiente e dizer se esta quente, ameno ou frio
# Se a temperatura for maior que 25 esta quente
# Se a temperatura for entre 18 e 24 esta ameno
# Se a temperatura for menor que 18 esta frio

time.sleep(1)
print ('Exercicio Tempereratura (2)')
temperatura = float(input('Qual a temperatura ambiente: '))
if (temperatura > 25):
    print ('Esta quente')
elif 24 >= temperatura >= 18:
    print ('Esta ameno')
else:
    print ('Esta frio')


# Exercicio 3
# Tem um filme de terror que tem 18 anos e e necessario ter ingresso para entrada
# Pegar Idade
# Pegar ingresso
# Verificar se tem ingresso e se tem idade para entrar

time.sleep(1)
idade = int(input('Qual sua idade: '))
ingresso = input('Voce tem ingresso? (s/n): ')
if (idade >= 18 and ingresso == 's'):
    print ('Voce pode entrar')
else:
    print ('Voce nao pode entrar')