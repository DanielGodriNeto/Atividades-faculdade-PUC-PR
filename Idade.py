Aniversario = float(input('Voce ja fez aniversario se sim 0 se nao 1:'))
nascimento = float(input("Coloque seu ano de nascimento: "))
Idade = 2026 - nascimento - Aniversario
print ('idade', Idade)

carros = float(input('Qauntos carros voce deseja alugar:'))
Total = carros * 100
print ('Total a pagar:', Total)

celcius = float(input('Quantos graus esta em celcius'))
firenhart = celcius * 1.8 + 32
print ('Agora esta', firenhart ,'Graus Fahrenheit')

nota1 = float(input('Qual a primeira nota: '))
nota2 = float(input('Qual a segunda nota: '))
nota3 = float(input('Qual a terceira nota: '))
nota4 = float(input('Qual a quarta nota: '))
notaF = (nota1 + nota2 + nota3 + nota4)/4
print ('Sua media e', notaF)

Idade2 = float(input('Quantos anos vc tem:'))
meses = float(input('Quantos meses alem dos anos voce tem:'))
Idademeses = (Idade2*12) + meses
print ('Sua idade em meses e', Idademeses)

peso = float(input('Qual o peso do produto em KG:'))
valor = float(input('Qual o valor do produto por KG:'))
preco = peso * valor
print ('esse e o valor do item', preco)