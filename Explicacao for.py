# #1 Tarefa basico do "for" em Python.

for i in range(1, 11):
    print(i)

for i in range(10, 0, -1):
    print(i)

#     #2 Tarefa comparacao com "for" em Python.

for i in range(1, 11):
    if i % 2 != 0:
        print(f"{i} é ímpar.")
    else:
        print(f"{i} é par.")

#Peça ao usuário que digite uma
#palavra que comece com uma
#vogal. Não permita que o programa
#continue se a palavra não for
#válida.
#Após isso, imprima no console cada
#letra da palavra em uma linha

palavra = input("Digite uma palavra: ")
if palavra[0] in "aeiou":
    for i in palavra:
        print(i)
else:
    print("A palavra não começa com uma vogal.")