from grammar import Grammar
from finite_automaton import *

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


# Check the 'accepts' method with other FA
# Define the finite automaton components
states = {'q0', 'q1', 'q2'}
alphabet = {'0', '1'}
transition_function = {
    ('q0', '0'): 'q0',
    ('q0', '1'): 'q1',
    ('q1', '0'): 'q2',
    ('q1', '1'): 'q0',
    ('q2', '0'): 'q1',
    ('q2', '1'): 'q2'
}
start_state = 'q0'
accept_states = {'q2'}

# Create the finite automaton
fa = FiniteAutomaton(states, alphabet, transition_function, start_state, accept_states)

# Test the finite automaton with different strings
test_strings = ['01', '010', '0101', '1111', '000', '110', '1100']
for string in test_strings:
    result = fa.accepts(string)
    print(f"String '{string}' is accepted: {result}")
