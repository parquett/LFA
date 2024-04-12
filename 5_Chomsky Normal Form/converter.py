class ChomskyNormalForm:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.new_variables = set(variables)

    def convert_to_cnf(self):
        self.remove_null_productions()
        self.remove_unit_productions()
        self.convert_to_proper_form()
        return self.productions

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

    def find_nullable_subsets(self, production, nullable):
        if not production:
            return {''}
        first, rest = production[0], production[1:]
        subsets = self.find_nullable_subsets(rest, nullable)
        if first in nullable:
            return subsets | {first + subset for subset in subsets}
        else:
            return {first + subset for subset in subsets}

    def remove_unit_productions(self):
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
