import unittest
from converter import ChomskyNormalForm
class TestChomskyNormalForm(unittest.TestCase):

    def sort_productions(self, productions):
        """ Helper function to sort the lists in the production dictionary. """
        return {key: sorted(value) for key, value in productions.items()}

    def test_remove_null_productions(self):
        variables = {'S', 'A', 'B'}
        terminals = {'a', 'b'}
        productions = {
            'S': ['AB', 'ε'],
            'A': ['a', 'ε'],
            'B': ['b']
        }
        start_symbol = 'S'
        cnf = ChomskyNormalForm(variables, terminals, productions, start_symbol)
        cnf.remove_null_productions()
        expected_productions = {
            'S': ['AB', 'B'],
            'A': ['a'],
            'B': ['b']
        }
        self.assertDictEqual(self.sort_productions(cnf.productions), self.sort_productions(expected_productions))

    def test_remove_unit_productions(self):
        variables = {'S', 'A', 'B'}
        terminals = {'a', 'b'}
        productions = {
            'S': ['A', 'B'],
            'A': ['a'],
            'B': ['A']  # Unit production
        }
        start_symbol = 'S'
        cnf = ChomskyNormalForm(variables, terminals, productions, start_symbol)
        cnf.remove_unit_productions()
        expected_productions = {
            'S': ['a', 'A'],
            'A': ['a'],
            'B': ['a']
        }
        self.assertDictEqual(self.sort_productions(cnf.productions), self.sort_productions(expected_productions))

    def test_convert_to_proper_form(self):
        variables = {'S'}
        terminals = {'a', 'b', 'c'}
        productions = {
            'S': ['abc']  # Longer than 2 symbols
        }
        start_symbol = 'S'
        cnf = ChomskyNormalForm(variables, terminals, productions, start_symbol)
        cnf.convert_to_proper_form()
        expected_productions = {
            'S': ['X1c'],
            'X1': ['ab']
        }
        self.assertDictEqual(self.sort_productions(cnf.productions), self.sort_productions(expected_productions))

    def test_full_conversion_to_cnf(self):
        variables = {'S', 'A', 'B', 'C'}
        terminals = {'a', 'b'}
        productions = {
            'S': ['AB', 'BC'],
            'A': ['a', 'ε'],
            'B': ['b', 'S'],
            'C': ['c', 'ε']
        }
        start_symbol = 'S'
        cnf = ChomskyNormalForm(variables, terminals, productions, start_symbol)
        cnf_productions = cnf.convert_to_cnf()
        expected_productions = {
            'S': ['b', 'S', 'AB', 'BC'],
            'A': ['a'],
            'B': ['b', 'S', 'AB', 'BC'],
            'C': ['c']
        }
        self.assertDictEqual(self.sort_productions(cnf_productions), self.sort_productions(expected_productions))

if __name__ == '__main__':
    unittest.main()
