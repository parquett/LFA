from lexer import Lexer, EOF

input_text = "12 + 24 - 8"
lexer = Lexer(input_text)
token = lexer.tokenize()
while token.type != EOF:
    print(token)
    token = lexer.tokenize()


