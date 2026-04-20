# Propositional formula representation
# Represent formulas as a tree of objects
# need classes for: Atom, Not, And, Or, Implies, Biconditional

class Formula:
    pass

class Atom(Formula):
    def __init__(self, name):
        self.name = name

class Not(Formula):
    def __init__(self, operand):
        self.operand = operand

class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Implies(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Biconditional(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
