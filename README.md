# Validador de Expressões em Lógica Proposicional (RA1)

Este projeto consiste em um analisador léxico e sintático para expressões de lógica proposicional escritas em LaTeX, conforme os requisitos da avaliação RA1.

## Alunos

- Fabrício Guite Pereira  
- Vinicius Guidotti Macedo

## Objetivo

Validar expressões proposicionais verificando se estão **lexica e gramaticalmente corretas**, utilizando:

- Um **analisador léxico** implementado como **máquina de estados finitos**.
- Um **parser LL(1)** recursivo para verificar a estrutura conforme a gramática fornecida.

## Gramática Utilizada

```bnf
FORMULA           ::= CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA  
CONSTANTE         ::= true | false  
PROPOSICAO        ::= [0-9][0-9a-z]*  
FORMULAUNARIA     ::= ( \neg FORMULA )  
FORMULABINARIA    ::= ( OPERADORBINARIO FORMULA FORMULA )  
OPERADORBINARIO   ::= \wedge | \vee | \rightarrow | \leftrightarrow  
