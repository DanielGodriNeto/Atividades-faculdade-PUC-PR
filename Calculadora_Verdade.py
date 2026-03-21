# ============================================
# CALCULADORA DE TABELA VERDADE
# ============================================
# Para rodar: python tabela_verdade.py
# Simbolos aceitos:
#   →  ou ->     implicacao
#   ↔  ou <->    bicondicional
#   ∧  ou &      e (AND)
#   ∨  ou |      ou (OR)
#   ¬  ou ~      nao (NOT)
# ============================================

import itertools
# itertools e uma biblioteca do Python que tem ferramentas para trabalhar
# com combinacoes e permutacoes. Vamos usar o itertools.product para
# gerar todas as combinacoes binarias possiveis (00, 01, 10, 11...).


# ===========================================
# PARTE 1: TOKENIZADOR
# ===========================================
# PROBLEMA: o Python nao entende "p → q" diretamente.
# SOLUCAO: dividir a string em pedacos chamados "tokens".
#
# Pense assim: quando voce le a frase "o gato comeu o peixe",
# seu cerebro automaticamente separa em palavras: ["o", "gato", "comeu", "o", "peixe"].
# O tokenizador faz a mesma coisa com a expressao logica.
#
# Exemplo:
#   entrada:  "p → (q & r)"
#   saida:    ['p', '->', '(', 'q', '&', 'r', ')']
#
# Por que transformar em lista? Porque e muito mais facil processar
# uma lista de tokens do que ficar olhando caractere por caractere
# na string original.

def tokenizar(expr):
    tokens = []  # lista vazia que vamos preenchendo
    i = 0        # indice que anda pela string caractere a caractere

    while i < len(expr):

        if expr[i] == ' ':
            i += 1  # espaco: apenas ignora e avanca

        elif expr[i:i+3] == '<->':
            # expr[i:i+3] pega uma "fatia" de 3 caracteres a partir de i.
            # Se for '<->' e o bicondicional em texto.
            # Adicionamos o token '<->' e avancamos 3 posicoes.
            tokens.append('<->'); i += 3

        elif expr[i:i+2] == '->':
            # Mesmo raciocinio: fatia de 2 caracteres.
            # '->' e a implicacao em texto.
            tokens.append('->'); i += 2

        elif expr[i] == '→':
            # Simbolo unicode da implicacao (1 caractere so).
            # Convertemos para '->' para padronizar tudo.
            tokens.append('->'); i += 1

        elif expr[i] == '↔':
            # Simbolo unicode do bicondicional.
            # Convertemos para '<->' para padronizar.
            tokens.append('<->'); i += 1

        elif expr[i] in ('∧', '&'):
            # 'in' verifica se o caractere esta dentro da tupla.
            # Aceita tanto o simbolo unicode ∧ quanto o & do teclado.
            # Ambos viram '&' para padronizar.
            tokens.append('&'); i += 1

        elif expr[i] in ('∨', '|'):
            # Mesmo raciocinio: aceita ∨ ou |, ambos viram '|'.
            tokens.append('|'); i += 1

        elif expr[i] in ('¬', '~', '!'):
            # Tres formas de escrever NOT. Todas viram '~'.
            tokens.append('~'); i += 1

        elif expr[i] in '()':
            # Parenteses sao importantes para definir precedencia.
            # Ex: (p & q) → r  e diferente de  p & (q → r)
            # Guardamos o parentese como token mesmo.
            tokens.append(expr[i]); i += 1

        elif expr[i].isalpha():
            # isalpha() retorna True se o caractere e uma letra (a-z, A-Z).
            # Letras sao as variaveis logicas: p, q, r, s...
            tokens.append(expr[i]); i += 1

        else:
            i += 1  # qualquer outro caractere desconhecido: ignora

    return tokens
    # Ao final, retornamos a lista de tokens pronta para o Parser usar.


# ===========================================
# PARTE 2: PARSER (interpretador)
# ===========================================
# PROBLEMA: agora temos a lista de tokens, mas ainda precisamos
# calcular o valor logico da expressao.
#
# SOLUCAO: Parser Recursivo Descendente.
#
# A ideia central e PRECEDENCIA: assim como em matematica
# 2 + 3 * 4 = 14 (nao 20), porque * tem prioridade sobre +,
# na logica tambem existe ordem de prioridade:
#
#   MAIOR prioridade (calculado primeiro):
#   1. ~ (NOT)         ex: ~p
#   2. & (AND)         ex: p & q4
#   3. | (OR)          ex: p | q
#   4. -> (implicacao) ex: p -> q
#   5. <-> (bicond.)   ex: p <-> q
#   MENOR prioridade (calculado por ultimo)
#
# Como implementar isso? Cada operacao vira um metodo que
# CHAMA O PROXIMO NIVEL antes de calcular o seu proprio resultado.
# Isso garante que operacoes de maior prioridade sejam resolvidas antes.
#
# Exemplo de como os metodos se encadeiam:
#   parse() chama impl()
#     impl() chama disjunc()
#       disjunc() chama conjunc()
#         conjunc() chama neg()
#           neg() chama atom()  ← chega na variavel de verdade
#         conjunc() aplica &
#       disjunc() aplica |
#     impl() aplica ->
#   parse() aplica <->

class Parser:

    def __init__(self, tokens, valores):
        # tokens:  a lista que veio do tokenizador. Ex: ['p', '->', 'q']
        # valores: dicionario com o valor de cada variavel nessa linha da tabela.
        #          Ex: {'p': True, 'q': False}
        # pos:     um "marcador" que indica qual token estamos lendo agora.
        #          Comeca em 0 (primeiro token) e vai avancando.
        self.tokens  = tokens
        self.pos     = 0
        self.valores = valores

    def peek(self):
        # "Espiar" o token atual SEM avançar o marcador.
        # Usado para decidir qual caminho tomar sem "consumir" o token ainda.
        # Retorna None se chegamos no fim da lista.
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self):
        # Le o token atual E avanca o marcador para o proximo.
        # Chamamos isso quando temos certeza que queremos "usar" esse token.
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # --- NIVEL 1: bicondicional <-> (menor precedencia) ---
    def parse(self):
        # Este e o ponto de entrada. Comeca sempre pelo nivel de menor precedencia.
        # Primeiro calculamos o que esta a esquerda (chamando impl()).
        # Depois, se o proximo token for '<->', consumimos e calculamos o lado direito.
        # Repetimos enquanto houver '<->' (o while permite encadear: p<->q<->r).
        esq = self.impl()
        while self.peek() == '<->':
            self.consumir()            # consome o '<->'
            dir = self.impl()
            esq = (esq == dir)
            # Por que == ?
            # A <-> B e verdadeiro quando os dois tem o MESMO valor.
            # True == True → True
            # False == False → True
            # True == False → False
            # Isso e exatamente a definicao do bicondicional!
        return esq

    # --- NIVEL 2: implicacao -> ---
    def impl(self):
        esq = self.disjunc()          # calcula o lado esquerdo primeiro
        if self.peek() == '->':
            self.consumir()            # consome o '->'
            dir = self.impl()
            # ATENCAO: chamamos self.impl() de novo (nao self.disjunc()).
            # Isso faz a implicacao ASSOCIAR A DIREITA.
            # p -> q -> r  e interpretado como  p -> (q -> r)
            # Se chamassemos disjunc(), seria (p -> q) -> r  (errado!)
            return (not esq) or dir
            # Por que (not esq) or dir ?
            # A implicacao A -> B so e FALSA quando A e True e B e False.
            # Em todas as outras combinacoes e True.
            # A tabela verdade:
            #   A=0 B=0 → 1   (not 0) or 0 = True or False = True  ✓
            #   A=0 B=1 → 1   (not 0) or 1 = True or True  = True  ✓
            #   A=1 B=0 → 0   (not 1) or 0 = False or False= False ✓
            #   A=1 B=1 → 1   (not 1) or 1 = False or True = True  ✓
        return esq

    # --- NIVEL 3: OR | ---
    def disjunc(self):
        esq = self.conjunc()
        while self.peek() == '|':
            self.consumir()            # consome o '|'
            esq = esq or self.conjunc()
            # OR e True se PELO MENOS UM dos lados for True.
            # O 'or' do Python faz exatamente isso.
            # O while permite encadear: p | q | r
        return esq

    # --- NIVEL 4: AND & ---
    def conjunc(self):
        esq = self.neg()
        while self.peek() == '&':
            self.consumir()            # consome o '&'
            esq = esq and self.neg()
            # AND e True somente se OS DOIS lados forem True.
            # O 'and' do Python faz exatamente isso.
            # O while permite encadear: p & q & r
        return esq

    # --- NIVEL 5: NOT ~ ---
    def neg(self):
        if self.peek() == '~':
            self.consumir()            # consome o '~'
            return not self.neg()
            # Chamamos self.neg() de novo (recursao)!
            # Isso permite ~~p (dupla negacao) funcionar corretamente:
            #   neg() ve '~', consome, chama neg() de novo
            #     neg() ve '~', consome, chama neg() de novo
            #       neg() ve 'p', retorna True (ex)
            #     retorna not True = False
            #   retorna not False = True   ← dupla negacao = original!
        return self.atom()            # se nao tem '~', vai para o proximo nivel

    # --- NIVEL 6: variavel ou parenteses (maior precedencia) ---
    def atom(self):
        # Este e o nivel mais basico: ou e uma variavel, ou e algo entre parenteses.
        tok = self.peek()

        if tok == '(':
            self.consumir()            # consome o '('
            val = self.parse()
            # Chamamos parse() de novo! Isso e o "recursivo" do parser.
            # Tudo dentro dos parenteses e calculado do zero,
            # como se fosse uma expressao independente.
            self.consumir()            # consome o ')' que fecha
            return val

        elif tok and tok.isalpha():
            # E uma variavel (p, q, r...).
            self.consumir()            # consome a variavel
            return self.valores[tok]
            # Buscamos o valor dela no dicionario.
            # Ex: self.valores['p'] retorna True ou False
            # dependendo da linha da tabela que estamos calculando.

        else:
            raise ValueError(f"Token inesperado: '{tok}'")
            # Se chegamos aqui, a expressao tem um erro de sintaxe.
            # Ex: "p → → q" teria dois '->' seguidos, o segundo causaria isso.


# ===========================================
# PARTE 3: GERADOR DE TABELA
# ===========================================
# PROBLEMA: queremos calcular a expressao para TODOS os valores possiveis.
# SOLUCAO: gerar todas as combinacoes binarias e calcular cada uma.
#
# Com n variaveis, temos 2^n combinacoes:
#   1 variavel  → 2 linhas  (0, 1)
#   2 variaveis → 4 linhas  (00, 01, 10, 11)
#   3 variaveis → 8 linhas  (000, 001, 010, 011, 100, 101, 110, 111)

def gerar_tabela(expressao):

    # PASSO 1: tokenizar a expressao
    tokens = tokenizar(expressao)
    # Ex: "p → q"  →  ['p', '->', 'q']

    # PASSO 2: encontrar as variaveis unicas na expressao
    variaveis = sorted(set(t for t in tokens if t.isalpha()))
    # Explicando essa linha:
    #   t for t in tokens     → percorre cada token
    #   if t.isalpha()        → filtra so as letras (variaveis)
    #   set(...)              → remove duplicatas (p & p vira so um 'p')
    #   sorted(...)           → ordena alfabeticamente (p, q, r...)
    # Ex: ['p', '->', 'q', '&', 'p']  →  ['p', 'q']

    if not variaveis:
        print("Nenhuma variavel encontrada.\n")
        return

    # PASSO 3: imprimir o cabecalho
    cabecalho = "  ".join(variaveis) + "  |  " + expressao
    print("\n" + cabecalho)
    print("-" * max(len(cabecalho), 20))

    tautologia  = True   # assume tautologia ate provar o contrario
    contradicao = True   # assume contradicao ate provar o contrario

    # PASSO 4: gerar todas as combinacoes e calcular cada linha
    for combo in itertools.product([0, 1], repeat=len(variaveis)):
        # itertools.product([0, 1], repeat=2) gera:
        #   (0, 0), (0, 1), (1, 0), (1, 1)
        # Exatamente as 4 linhas de uma tabela com 2 variaveis!
        # Para 3 variaveis (repeat=3), geraria 8 combinacoes, etc.

        # PASSO 4a: montar o dicionario de valores para essa linha
        valores = {v: bool(c) for v, c in zip(variaveis, combo)}
        # zip(variaveis, combo) emparelha variavel com valor:
        #   zip(['p','q'], (0,1))  →  [('p',0), ('q',1)]
        # bool(0) = False, bool(1) = True
        # Resultado: {'p': False, 'q': True}

        # PASSO 4b: calcular a expressao com esses valores
        resultado = Parser(tokens, valores).parse()
        # Criamos um Parser novo para cada linha (pos volta a 0).
        # .parse() inicia o calculo pelo nivel de menor precedencia
        # e retorna True ou False.

        # PASSO 4c: imprimir a linha
        bits = "  ".join(str(int(c)) for c in combo)
        # int(c) converte 0/1 (ja sao int, mas garantimos)
        # str(...) converte para string para o join funcionar
        # "  ".join(...) separa com dois espacos: "0  1"
        res = int(resultado)
        # int(True) = 1, int(False) = 0
        print(f"  {bits}  |  {res}")

        # PASSO 4d: verificar se e tautologia ou contradicao
        if res == 0: tautologia  = False
        # Se achou pelo menos um 0, nao pode ser tautologia
        if res == 1: contradicao = False
        # Se achou pelo menos um 1, nao pode ser contradicao

    # PASSO 5: imprimir a conclusao
    print()
    if tautologia:
        print("TAUTOLOGIA: sempre verdadeiro")
    elif contradicao:
        print("CONTRADICAO: sempre falso")
    else:
        print("CONTINGENCIA: depende dos valores das variaveis")


# ===========================================
# MENU PRINCIPAL
# ===========================================

def main():
    print("=" * 50)
    print("  CALCULADORA DE TABELA VERDADE")
    print("=" * 50)
    print("Simbolos: →  ↔  ∧  ∨  ¬  (ou -> <-> & | ~)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        expressao = input("Expressao: ").strip()
        # .strip() remove espacos em branco no inicio e fim da string

        if expressao.lower() == "sair":
            # .lower() converte para minusculo, entao "SAIR" e "Sair" tambem funcionam
            print("Ate logo!")
            break

        if not expressao:
            continue  # se o usuario so apertou Enter, pede de novo

        try:
            gerar_tabela(expressao)
        except Exception as e:
            # Se o usuario digitou algo invalido, mostramos o erro
            # sem deixar o programa travar.
            print(f"Erro: {e}")

        print()  # linha em branco para separar visualmente

main()