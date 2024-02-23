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


# Convert FA to Regular Grammar
def fa_to_rg(Q, Sigma, F, delta):
    grammar = {}
    for state in Q:
        for input_symbol in Sigma:
            if (state, input_symbol) in delta:
                for next_state in delta[(state, input_symbol)]:
                    # Production rule: state -> input_symbol next_state
                    if state not in grammar:
                        grammar[state] = []
                    grammar[state].append(f"{input_symbol}{next_state if next_state not in F else ''}")
    # Add final state production rule
    for final_state in F:
        if final_state not in grammar:
            grammar[final_state] = []
        grammar[final_state].append('ε')
    return grammar


# Check if our FA is DFA or NDFA
print("Is DFA:", is_dfa(Q, Sigma, delta))

# Convert our FA to regular grammar
rg = fa_to_rg(Q, Sigma, F, delta)
print("Regular Grammar:", rg)

