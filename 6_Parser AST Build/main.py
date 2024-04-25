from my_lexer import Lexer
from my_parser import Parser
from my_ast import print_ast


text = "3 + 5 - 2"
lexer = Lexer(text)
lexer.tokenize()
parser = Parser(lexer)
ast = parser.parse()

print("Tokens:")
for token in lexer.tokens:
    print(token)

print("\nAST:")
print_ast(ast)



