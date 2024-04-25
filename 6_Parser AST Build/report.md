# Topic: Parser & Building an Abstract Syntax Tree

----

## Overview
The process of gathering syntactical meaning or doing a syntactical analysis over some text can also be called parsing.
It usually results in a parse tree which can also contain semantic information that could be used in subsequent stages
of compilation, for example.

Similarly to a parse tree, in order to represent the structure of an input text one could create an Abstract Syntax 
Tree (AST). This is a data structure that is organized hierarchically in abstraction layers that represent the 
constructs or entities that form up the initial text. These can come in handy also in the analysis of programs or some
processes involved in compilation.


## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed.
2. Get familiar with the concept of AST.
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

---

## Implementation Explanation

The lexer, or lexical analyzer, is a crucial component in compilers and interpreters, transforming a sequence of
characters into a series of tokens. These tokens are utilized by parsers to construct meaningful structures, such as 
abstract syntax trees. The provided implementation illustrates a simple lexer aimed at tokenizing basic arithmetic expressions.
Below is a detailed explanation of its components and functionality:

### Token Class
- **Purpose**: Represents the smallest meaningful unit within the input text, such as numbers, operators, or an 
end-of-file (EOF) marker.
- **Attributes**:
  - `type`: Identifies the token type (e.g., INTEGER, PLUS, MINUS, EOF).
  - `value`: Contains the actual value represented by the token, which could be a character like '+' or '-', 
  a numerical value, or `None` for the EOF token.
```python
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.name}, {repr(self.value)})'
```

### Lexer Class
- **Purpose**: Scans the input string to produce tokens using regex.

```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.tokens = []

    def error(self):
        raise Exception('Invalid character')

    def tokenize(self):
        # Regular expressions for tokens
        token_specification = [
            (TokenType.INTEGER, r'\d+'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'\-'),
            (TokenType.EOF, r'\Z')
        ]

        # Create a regex that matches the token specifications
        token_regex = '|'.join(f'(?P<{tok.name}>{pattern})' for tok, pattern in token_specification)
        for mo in re.finditer(token_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            tok_type = TokenType[kind]
            if tok_type == TokenType.INTEGER:
                value = int(value)  # Convert to integer
            self.tokens.append(Token(tok_type, value))

        self.tokens.append(Token(TokenType.EOF, None))
```

### Parser Class
- **Purpose**: Analyzes a sequence of tokens to create an AST representing the syntactic structure of the input.
- **Functionality**: The parser processes tokens to identify the grammar's structures, handling precedence and associativity 
of operators. It constructs an AST where each node represents a grammatical construct (e.g., a binary operation or a number).
```python
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TokenType.EOF, None)

    def error(self):
        raise Exception('Invalid syntax')

    def parse(self):
        if self.current_token.type == TokenType.EOF:
            return None

        left = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.advance()
            right = self.term()
            left = BinOp(left=left, op=op, right=right)
        return left

    def term(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.advance()
            return Num(token)
        else:
            self.error()
```

### AST Class
- **Purpose**: Defines the nodes of the AST, each representing a different construct (e.g., binary operations, numbers).
- *Nodes*:
   - BinOp: Represents binary operations with two operands and an operator.
   - Num: Represents numbers.
```python
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
```

### Example Usage
The `main` function demonstrates the lexer, parser, and AST in action, parsing a simple arithmetic expression into a structured tree.

```python
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
```

### Summary
The lexer utilizes enumeration and regular expressions to identify tokens, the parser processes these tokens to 
understand the input's syntactic structure, and the AST represents this structure in a tree form. The demonstration of 
the lexer, parser, and AST illustrates their collective operation and showcases the fundamental mechanisms of language 
processing in compilers and interpreters.
