import itertools

def tokenizar(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] == ' ':
            i += 1
        elif expr[i:i+3] == '<->':
            tokens.append('<->'); i += 3
        elif expr[i:i+2] == '->':
            tokens.append('->'); i += 2
        elif expr[i] == '→':
            tokens.append('->'); i += 1
        elif expr[i] == '↔':
            tokens.append('<->'); i += 1
        elif expr[i] in ('∧', '&'):
            tokens.append('&'); i += 1
        elif expr[i] in ('∨', '|'):
            tokens.append('|'); i += 1
        elif expr[i] in ('¬', '~', '!'):
            tokens.append('~'); i += 1
        elif expr[i] in '()':
            tokens.append(expr[i]); i += 1
        elif expr[i].isalpha():
            tokens.append(expr[i]); i += 1
        else:
            i += 1
    return tokens


class Parser:

    def __init__(self, tokens, valores):
        self.tokens  = tokens
        self.pos     = 0
        self.valores = valores

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        esq = self.impl()
        while self.peek() == '<->':
            self.consumir()
            dir = self.impl()
            esq = (esq == dir)
        return esq

    def impl(self):
        esq = self.disjunc()
        if self.peek() == '->':
            self.consumir()
            dir = self.impl()
            return (not esq) or dir
        return esq

    def disjunc(self):
        esq = self.conjunc()
        while self.peek() == '|':
            self.consumir()
            esq = esq or self.conjunc()
        return esq

    def conjunc(self):
        esq = self.neg()
        while self.peek() == '&':
            self.consumir()
            esq = esq and self.neg()
        return esq

    def neg(self):
        if self.peek() == '~':
            self.consumir()
            return not self.neg()
        return self.atom()

    def atom(self):
        tok = self.peek()
        if tok == '(':
            self.consumir()
            val = self.parse()
            self.consumir()
            return val
        elif tok and tok.isalpha():
            self.consumir()
            return self.valores[tok]
        else:
            raise ValueError(f"Token inesperado: '{tok}'")


def gerar_tabela(expressao):
    tokens    = tokenizar(expressao)
    variaveis = sorted(set(t for t in tokens if t.isalpha()))

    if not variaveis:
        print("Nenhuma variavel encontrada.\n")
        return

    cabecalho = "  ".join(variaveis) + "  |  " + expressao
    print("\n" + cabecalho)
    print("-" * max(len(cabecalho), 20))

    tautologia  = True
    contradicao = True

    for combo in itertools.product([0, 1], repeat=len(variaveis)):
        valores   = {v: bool(c) for v, c in zip(variaveis, combo)}
        resultado = Parser(tokens, valores).parse()
        bits = "  ".join(str(int(c)) for c in combo)
        res  = int(resultado)
        print(f"  {bits}  |  {res}")
        if res == 0: tautologia  = False
        if res == 1: contradicao = False

    print()
    if tautologia:
        print("TAUTOLOGIA: sempre verdadeiro")
    elif contradicao:
        print("CONTRADICAO: sempre falso")
    else:
        print("CONTINGENCIA: depende dos valores das variaveis")


def main():
    print("=" * 50)
    print("  CALCULADORA DE TABELA VERDADE")
    print("=" * 50)
    print("Simbolos: →  ↔  ∧  ∨  ¬  (ou -> <-> & | ~)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        expressao = input("Expressao: ").strip()
        if expressao.lower() == "sair":
            print("Ate logo!")
            break
        if not expressao:
            continue
        try:
            gerar_tabela(expressao)
        except Exception as e:
            print(f"Erro: {e}")
        print()

main()