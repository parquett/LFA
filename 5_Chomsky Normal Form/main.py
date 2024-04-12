from converter import ChomskyNormalForm

# test my variant
variables = {'S', 'A', 'B', 'C', 'D'}
terminals = {'a', 'b'}
productions = {
    'S': ['aB', 'DA'],
    'A': ['a', 'BD', 'bDAB'],
    'B': ['b', 'BA'],
    'C': ['BA'],
    'D': ['ε', 'BA']
}
start_symbol = 'S'

cnf_converter = ChomskyNormalForm(variables, terminals, productions, start_symbol)
cnf_productions = cnf_converter.convert_to_cnf()
print(cnf_productions)