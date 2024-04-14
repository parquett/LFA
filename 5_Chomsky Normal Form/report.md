# Topic: Chomsky Normal Form

----

## Overview

Chomsky Normal Form (CNF) is a specific form of context-free grammars where every production rule is in one of two forms:
1. A non-terminal symbol (variable) directly produces two non-terminal symbols.
2. A non-terminal symbol directly produces a terminal symbol. 

In CNF, there are no null productions (productions that derive the empty string) or unit productions (productions where
a single non-terminal symbol derives another non-terminal symbol). CNF simplifies grammar representations and 
facilitates efficient parsing algorithms.


## Objectives:
1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   2. The implemented functionality needs executed and tested.
   3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
   4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

---

## Implementation Explanation

he Chomsky Normal Form (CNF) is a standard form used in formal language theory. It simplifies the structure of 
context-free grammars by imposing specific restrictions on production rules. This report discusses the implementation 
of a Python class, ChomskyNormalForm, which facilitates the conversion of context-free grammars to Chomsky Normal Form.

###  Class Structure
- `variables`: Set of non-terminal symbols.
- `terminals`: Set of terminal symbols.
- `productions`: Dictionary representing the production rules of the grammar.
- `start_symbol`: The starting symbol of the grammar.

```python
class ChomskyNormalForm:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.new_variables = set(variables)
```

### Conversion Procces
The conversion to Chomsky Normal Form is carried out in three main steps, each implemented as a separate method:
  - `remove_null_productions`: Null productions are productions that derive the empty string ('ε'). This method removes 
null productions from the grammar and updates the production rules accordingly.
```python
    def remove_null_productions(self):
        nullable = set()
        for var, prods in self.productions.items():
            if 'ε' in prods:
                nullable.add(var)

        changes = True
        while changes:
            changes = False
            for var, prods in self.productions.items():
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        if var not in nullable:
                            nullable.add(var)
                            changes = True

        for var in list(self.productions):
            self.productions[var] = [prod for prod in self.productions[var] if prod != 'ε']
            new_prods = set()
            for prod in self.productions[var]:
                subsets = self.find_nullable_subsets(prod, nullable)
                new_prods.update(subsets)
            self.productions[var] = list(new_prods)
```
  - `remove_unit_productions`:Unit productions are productions where a single non-terminal symbol derives another 
non-terminal symbol. This method eliminates unit productions from the grammar by iteratively replacing them with their 
respective productions until no further changes can be made.
```python
        units = {var: {var} for var in self.productions}
        changes = True
        while changes:
            changes = False
            for var, prods in self.productions.items():
                for prod in prods:
                    if len(prod) == 1 and prod in self.variables:
                        new_units = units[var] | units[prod]
                        if new_units != units[var]:
                            units[var] = new_units
                            changes = True
        for var in units:
            self.productions[var] = [prod for prod in self.productions[var] if
                                     len(prod) != 1 or prod not in self.variables]
            for unit in units[var]:
                if unit != var:
                    self.productions[var].extend(self.productions[unit])
            self.productions[var] = list(set(self.productions[var]))
```
  - `convert_to_proper_form`: This method converts any remaining productions to proper Chomsky Normal Form. Productions 
with more than two non-terminals are split into smaller productions, each containing at most two non-terminals.

```python
    def convert_to_proper_form(self):
        for var in list(self.productions):
            new_prods = []
            for prod in self.productions[var]:
                if len(prod) <= 2:
                    new_prods.append(prod)
                else:
                    current_var = prod[0]
                    for i in range(1, len(prod) - 1):
                        new_var = 'X' + str(len(self.new_variables))
                        self.new_variables.add(new_var)
                        self.productions[new_var] = [current_var + prod[i]]
                        current_var = new_var
                    new_prods.append(current_var + prod[-1])
            self.productions[var] = list(set(new_prods))
```

### Implementation Details
- The `find_nullable_subsets` method recursively finds all nullable subsets of a production, given a set of nullable 
symbols.
```python
    def find_nullable_subsets(self, production, nullable):
        if not production:
            return {''}
        first, rest = production[0], production[1:]
        subsets = self.find_nullable_subsets(rest, nullable)
        if first in nullable:
            return subsets | {first + subset for subset in subsets}
        else:
            return {first + subset for subset in subsets}
```
- New non-terminal symbols are generated as 'X' followed by a unique integer to ensure they do not conflict with 
existing symbols.
- The class maintains a set of `new_variables` to keep track of newly introduced non-terminals during the conversion 
process.

### Example Usage
The `main` function demonstrates the usage of my class to perform conversion from Context Free Grammar to Chomsky Normal Form, 
according to my variant(13). However, it can convert whatever CFG, not only from my variant.

```python
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
```

### Unit Testing
- `test_remove_null_productions`: Tests the removal of null productions (productions that derive the empty string) from the 
grammar.
- `test_remove_unit_productions`: Tests the removal of unit productions (productions where a non-terminal directly produces 
another non-terminal) from the grammar.
- `test_convert_to_proper_form`: Tests the conversion of productions longer than two symbols into proper CNF form. In CNF, 
each production should have at most two symbols on the right-hand side.
- `test_full_conversion_to_cnf`: Tests the full conversion of a context-free grammar into Chomsky Normal Form.
- `sort_productions`: This helper method sorts the production rules within each non-terminal's list to ensure that 
order differences do not cause test failures. Each test uses this method to sort both the expected and actual 
productions before comparing them with `assertDictEqual`.

Each test case sets up a context-free grammar with certain productions, terminals, variables, and a start symbol. Then 
it applies a transformation or conversion method from the ChomskyNormalForm class and asserts that the resulting 
productions match the expected ones.

*Example of unit test:*
```python
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
```

### Summary
The `ChomskyNormalForm` class provides a comprehensive implementation for converting context-free grammars into Chomsky 
Normal Form. By following a systematic approach of removing null and unit productions and then converting the remaining 
productions to proper form, the resulting grammar adheres to the strict rules of CNF, facilitating efficient parsing 
algorithms and other applications in formal language theory.
