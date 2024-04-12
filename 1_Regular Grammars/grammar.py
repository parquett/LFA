import random

class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def generate(self, start, depth=5):
        if start not in self.VN or (depth == 0 and start not in self.P):
            return start
        else:
            production = random.choice(self.P.get(start, ['']))
            return ''.join(self.generate(s, depth - 1) for s in production)

    def classify(self):
        regular = True
        context_free = True
        context_sensitive = True
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # Adjusted checks for a list structure of rhs
                if not (len(rhs) == 1 and rhs[0] in self.VT) and not (len(rhs) == 2 and rhs[0] in self.VT and rhs[1] in self.VN):
                    regular = False
                if not (len(lhs) == 1 and lhs in self.VN):
                    context_free = False
                if len(rhs) < len(lhs):
                    context_sensitive = False
        if regular:
            return "Type 3 (Regular)"
        elif context_free:
            return "Type 2 (Context-Free)"
        elif context_sensitive:
            return "Type 1 (Context-Sensitive)"
        else:
            return "Type 0 (Recursively Enumerable)"
