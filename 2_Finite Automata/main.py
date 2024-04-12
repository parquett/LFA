import functions as func

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

# FA from previous Lab
# Q = ['F', 'B', 'D', 'S']
# Sigma = ['b', 'c', 'a']
# F = ['F']
# delta = {  # Transition function
#     ('B', 'a'): ['D'],
#     ('B', 'b'): ['B'],
#     ('B', 'C'): ['S'],  # Non-deterministic part
#     ('D', 'a'): ['D'],
#     ('D', 'b'): ['S'],
#     ('D', 'c'): ['F'],
#     ('S', 'a'): ['B']
# }


# Check if our FA is DFA or NDFA
print("Is DFA:", func.is_dfa(Q, Sigma, delta), "\n")

# Convert our FA to regular grammar
rg = func.fa_to_rg(Q, Sigma, F, delta)
print("Regular Grammar:", rg, "\n")

# Perform the conversion
dfa_states, dfa_sigma, dfa_final_states, dfa_delta = func.ndfa_to_dfa(Q, Sigma, F, delta)
print("DFA States:", dfa_states)
print("DFA Alphabet:", dfa_sigma)
print("DFA Final States:", dfa_final_states)
print("DFA Transition Function:", dfa_delta)
# Check the conversion
print("Is DFA:", func.is_dfa(dfa_states, dfa_sigma, dfa_delta))

# Visualize FA
func.visualize_ndfa(Q, Sigma, F, delta, "NDFA Visualization")
func.visualize_dfa(dfa_states, dfa_sigma, dfa_final_states, dfa_delta, "DFA Visualization")
