Q = ['q0', 'q1', 'q2', 'q3']  # States
Sigma = ['a', 'b']  # Alphabet
F = ['q3']  # Final states
delta = {  # Transition function
    ('q0', 'a'): ['q0'],
    ('q0', 'b'): ['q1'],
    ('q1', 'a'): ['q1', 'q2'],  # Non-deterministic part
    ('q1', 'b'): ['q3'],
    ('q2', 'a'): ['q2'],
    ('q2', 'b'): ['q3']
}

# Determine if FA is DFA or NDFA
def is_dfa(Q, Sigma, delta):
    for state in Q:
        for input_symbol in Sigma:
            if (state, input_symbol) in delta:
                if len(delta[(state, input_symbol)]) > 1:
                    return False  # NDFA
    return True  # DFA

# Check if our FA is DFA or NDFA
print("Is DFA:", is_dfa(Q, Sigma, delta))

