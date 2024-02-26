from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

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


def visualize_ndfa(Q, Sigma, F, delta, title="Finite Automaton"):
    G = nx.DiGraph()
    pos = {}
    for i, state in enumerate(Q):
        G.add_node(state)
        pos[state] = (i * 2, 0)  # Position nodes in a horizontal line

    for (start_state, input_symbol), end_states in delta.items():
        if isinstance(end_states, list):
            for end_state in end_states:
                G.add_edge(start_state, end_state, label=input_symbol)
        else:
            G.add_edge(start_state, end_states, label=input_symbol)

    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_weight='bold', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Highlight final states with a double circle
    final_state_pos = {state: pos[state] for state in F}
    nx.draw_networkx_nodes(G, final_state_pos, nodelist=F, node_shape='o', node_color='skyblue',
                           linewidths=2.0, edgecolors='black', node_size=2000)

    ax.set_title(title)
    plt.tight_layout()
    plt.axis('off')
    plt.show()


def visualize_dfa(Q, Sigma, F, delta, title="Finite Automaton"):
    G = nx.DiGraph()
    pos = {}
    node_labels = {}
    step = 0
    for state in Q:
        # Ensure unique positions for each state
        pos[state] = (step, 0)
        node_labels[state] = state
        step += 1

    # Add edges based on transitions
    for start_state, transitions in delta.items():
        for input_symbol, end_state in transitions.items():
            G.add_edge(start_state, end_state, label=input_symbol)

    edge_labels = nx.get_edge_attributes(G, 'label')
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the FA graph
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')

    # Draw double circles for final states
    for final_state in F:
        nx.draw_networkx_nodes(G, pos, nodelist=[final_state], node_size=1800, node_color='lightblue',
                               edgecolors='black', linewidths=2)

    ax.set_title(title)
    plt.tight_layout()
    plt.axis('off')
    plt.show()