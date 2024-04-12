# Topic: Lexer & Scanner

----

## Overview
&ensp;&ensp;&ensp;The term lexer comes from lexical analysis which, in turn, represents the process of extracting
lexical tokens from a string of characters. There are several alternative names for the mechanism called lexer, for 
example tokenizer or scanner. The lexical analysis is one of the first stages used in a compiler/interpreter when 
dealing with programming, markup or other types of languages. The tokens are identified based on some rules of the 
language and the products that the lexer gives are called lexemes. So basically the lexer is a stream of lexemes. 
Now in case it is not clear what's the difference between lexemes and tokens, there is a big one. The lexeme is just 
the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each 
lexeme. So the tokens don't retain necessarily the actual value of the lexeme, but rather the type of it and maybe some 
metadata.


## Objectives:
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

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

    # string representation
    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()
```

### Lexer Class
- **Purpose**: Scans the input string to identify and extract tokens.
- **Attributes**:
  - `text`: The string to be tokenized.
  - `pos`: The current position within the string.
  - `current_char`: The character at the current position.
- **Methods**:
  - `advance()`: Progresses to the next character in the input string or sets `current_char` to `None` if the end is 
  reached.
  - `skip_whitespace()`: Omits any whitespace characters by moving the current position forward until a non-whitespace 
  character is encountered.
  - `integer()`: Gathers a series of digit characters and converts them into an integer token, continuing until a 
  non-digit character is found.
  - `tokenize()`: The main method that determines the next token based on the current character. It decides to:
    - Skip whitespace.
    - Generate an INTEGER token for digit sequences.
    - Produce a PLUS or MINUS token for '+' or '-' characters, respectively.
    - Emit an error for unrecognized characters or return an EOF token if the end of the input is reached.

```python
class Lexer:
    # lexer class to tokenize the input
    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    # lexical tokenizer
    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)
```

### Example Usage
The `main` function demonstrates using the lexer with a simple arithmetic expression. It initializes the lexer with an 
input string and sequentially retrieves tokens until the EOF token is encountered, printing each token to display the 
lexer's operation.

```python
input_text = "12 + 24 - 8"
lexer = Lexer(input_text)
token = lexer.tokenize()
while token.type != EOF:
    print(token)
    token = lexer.tokenize()
```

### Summary
This lexer is designed with simplicity in mind, focusing on arithmetic expressions such as addition and subtraction.
Real-world lexers are typically more complex, dealing with a broader range of token types and the syntax nuances of the 
input language. This laboratory provides a foundational understanding of how lexers function: reading the input one 
character at a time, recognizing patterns that constitute tokens, and generating a stream of tokens for further analysis.
