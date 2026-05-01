# Propositional formula representation
# Represent formulas as a tree of objects
# need classes for: Atom, Not, And, Or, Implies, Biconditional


# formula.py (minimal version for testing)
class Formula:
    pass

class Atom(Formula):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Atom('{self.name}')"
    
    def __eq__(self, other):
        return isinstance(other, Atom) and self.name == other.name
    
    def __hash__(self):
        return hash(('Atom', self.name))

class Not(Formula):
    def __init__(self, operand):
        self.operand = operand
    
    def __repr__(self):
        return f"Not({self.operand})"
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand
    
    def __hash__(self):
        return hash(('Not', self.operand))

class BinaryFormula(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and 
                self.left == other.left and 
                self.right == other.right)
    
    def __hash__(self):
        return hash((self.__class__.__name__, self.left, self.right))

class And(BinaryFormula):
    pass

class Or(BinaryFormula):
    pass

class Implies(BinaryFormula):
    pass

class Biconditional(BinaryFormula):
    pass