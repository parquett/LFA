class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if (current_state, symbol) in self.transition_function:
                current_state = self.transition_function[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states

def convert_grammar_to_fa(grammar):
    states = grammar.VN.union({ 'F' })  # F is a new accept state
    alphabet = grammar.VT
    transition_function = {}
    start_state = 'S'
    accept_states = { 'F' }

    for non_terminal in grammar.VN:
        for production in grammar.P[non_terminal]:
            if len(production) == 1:  # A -> a
                transition_function[(non_terminal, production[0])] = 'F'
            else:  # A -> aB
                transition_function[(non_terminal, production[0])] = production[1]

    return FiniteAutomaton(states, alphabet, transition_function, start_state, accept_states)
