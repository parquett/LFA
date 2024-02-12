from grammar import Grammar
from finite_automaton import convert_grammar_to_fa

# Define the grammar
VN = {'S', 'B', 'D'}
VT = {'a', 'b', 'c'}
P = {
    'S': [['a', 'B']],
    'B': [['a', 'D'], ['b', 'B'], ['c', 'S']],
    'D': [['a', 'D'], ['b', 'S'], ['c']]
}

# Create an instance of the Grammar class
grammar = Grammar(VN, VT, P)

# Convert the grammar to a finite automaton
fa = convert_grammar_to_fa(grammar)

for _ in range(5):
    print(grammar.generate('S'))

print(fa.accepts('abc'))

