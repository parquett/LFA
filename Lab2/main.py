from collections import defaultdict

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


# Convert NDFA to DFA
def ndfa_to_dfa(Q, Sigma, F, delta):
    initial_state = ['q0']
    dfa_states = [initial_state]
    dfa_delta = {}
    dfa_final_states = []
    state_map = {'q0': initial_state}

    while dfa_states:
        current_dfa_state = dfa_states.pop(0)
        for input_symbol in Sigma:
            # Find the union of transitions for all NDFA states in the current DFA state
            next_states = set()
            for ndfa_state in current_dfa_state:
                if (ndfa_state, input_symbol) in delta:
                    next_states.update(delta[(ndfa_state, input_symbol)])
            next_states = sorted(list(next_states))

            if not next_states:
                continue

            # Check if these next states form a new DFA state
            dfa_state_name = ','.join(next_states)
            if dfa_state_name not in state_map:
                state_map[dfa_state_name] = next_states
                dfa_states.append(next_states)
                if any(state in F for state in next_states):
                    dfa_final_states.append(dfa_state_name)

            # Record the transition
            dfa_delta[(','.join(current_dfa_state), input_symbol)] = dfa_state_name

    # Convert delta to a more standard form
    dfa_delta_standardized = defaultdict(dict)
    for (state, symbol), next_state in dfa_delta.items():
        dfa_delta_standardized[state][symbol] = next_state

    return list(state_map.keys()), Sigma, dfa_final_states, dict(dfa_delta_standardized)


# Check if our FA is DFA or NDFA
print("Is DFA:", is_dfa(Q, Sigma, delta), "\n")

# Convert our FA to regular grammar
rg = fa_to_rg(Q, Sigma, F, delta)
print("Regular Grammar:", rg, "\n")

# Perform the conversion
dfa_states, dfa_sigma, dfa_final_states, dfa_delta = ndfa_to_dfa(Q, Sigma, F, delta)
print("DFA States:", dfa_states)
print("DFA Alphabet:", dfa_sigma)
print("DFA Final States:", dfa_final_states)
print("DFA Transition Function:", dfa_delta)
# Check the conversion
print("Is DFA:", is_dfa(dfa_states, dfa_sigma, dfa_delta))

