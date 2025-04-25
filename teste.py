# Alunos: Fabrício Guite Pereira, Vinicius Guidotti Macedo, Alexandre de Moraes Bueno

import sys

def lexer(expr):
    tokens = []
    estado = 'INICIO'
    i = 0
    buffer = ''

    while i < len(expr):
        c = expr[i]

        if estado == 'INICIO':
            if c.isspace():
                i += 1
            elif c == '(':
                tokens.append(('ABREPAREN', c))
                i += 1
            elif c == ')':
                tokens.append(('FECHAPAREN', c))
                i += 1
            elif c == '\\':
                estado = 'OPERADOR'
                buffer = c
                i += 1
            elif c.isdigit() or c.isalpha():
                buffer = c
                estado = 'TOKEN'
                i += 1
            else:
                raise ValueError(f"Caractere inválido na posição {i}: {c}")

        elif estado == 'OPERADOR':
            buffer += c
            i += 1
            if buffer in ['\\neg', '\\wedge', '\\vee', '\\rightarrow', '\\leftrightarrow']:
                token = 'OPUNARIO' if buffer == '\\neg' else 'OPBINARIO'
                tokens.append((token, buffer))
                buffer = ''
                estado = 'INICIO'

        elif estado == 'TOKEN':
            if c.isalnum():
                buffer += c
                i += 1
            else:
                if buffer in ['true', 'false']:
                    tokens.append(('CONSTANTE', buffer))
                else:
                    tokens.append(('PROPOSICAO', buffer))
                buffer = ''
                estado = 'INICIO'

    if estado == 'TOKEN':
        if buffer in ['true', 'false']:
            tokens.append(('CONSTANTE', buffer))
        else:
            tokens.append(('PROPOSICAO', buffer))

    elif estado == 'OPERADOR':
        if buffer in ['\\neg', '\\wedge', '\\vee', '\\rightarrow', '\\leftrightarrow']:
            token = 'OPUNARIO' if buffer == '\\neg' else 'OPBINARIO'
            tokens.append((token, buffer))
        else:
            raise ValueError(f"Operador inválido: {buffer}")

    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        try:
            self.formula()
            if self.pos != len(self.tokens):
                raise Exception("Tokens restantes após o fim da análise")
            return True
        except Exception:
            return False

    def consume(self, expected_type):
        if self.match(expected_type):
            self.pos += 1
        else:
            raise Exception(f"Esperado {expected_type}, encontrado {self.tokens[self.pos] if self.pos < len(self.tokens) else 'EOF'}")

    def match(self, token_type):
        return self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type

    def formula(self):
        if self.match('CONSTANTE'):
            self.consume('CONSTANTE')
        elif self.match('PROPOSICAO'):
            self.consume('PROPOSICAO')
        elif self.match('ABREPAREN'):
            self.consume('ABREPAREN')
            if self.match('OPUNARIO'):
                self.consume('OPUNARIO')
                self.formula()
                self.consume('FECHAPAREN')
            elif self.match('OPBINARIO'):
                self.consume('OPBINARIO')
                self.formula()
                self.formula()
                self.consume('FECHAPAREN')
            else:
                raise Exception('Operador inválido após "("')
        else:
            raise Exception('Início de fórmula inválido')

def main():
    if len(sys.argv) != 2:
        print("Uso: python validador.py <arquivo>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        sys.exit(1)

    try:
        num_expressoes = int(linhas[0].strip())
    except ValueError:
        print("A primeira linha deve conter um número inteiro.")
        sys.exit(1)

    expressoes = linhas[1:num_expressoes+1]

    for expr in expressoes:
        try:
            tokens = lexer(expr.strip())
            parser = Parser(tokens)
            resultado = parser.parse()
            print("valida" if resultado else "invalida")
        except Exception:
            print("invalida")

if __name__ == "__main__":
    main()
