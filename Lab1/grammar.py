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
