# formula.py
#
# Propositional formula representation as a tree of objects.
#
# Each formula is an instance of a class that inherits from Formula.
# The classes are:
# - Atom: represents a propositional variable (e.g., P, Q, R)
# - Not: represents negation (¬)
# - And: represents conjunction (∧)
# - Or: represents disjunction (∨)
# - Implies: represents implication (→)
# - Biconditional: represents biconditional (↔)
#
# Each class has an __init__ method to initialize its fields, and an __eq__ method to compare formulas for equality.
# The __hash__ method is implemented to allow formulas to be used as keys in dictionaries and sets.
# The __str__ and __repr__ methods are implemented to provide readable string representations of the formulas.


class Formula:
    """
    Base class for all propositional logic formulas.
    All concrete classes below inherit from this.
    """
    def __repr__(self) -> str:
        raise NotImplementedError
 
    def __eq__(self, other) -> bool:
        raise NotImplementedError
 
    def __hash__(self) -> int:
        raise NotImplementedError
 
    def atoms(self) -> set:
        """Return the set of all propositional variable names in this formula."""
        raise NotImplementedError

class Atom(Formula):
    """
    Represents a propositional variable (e.g., P, Q, R).

    Example:
        Atom('p') represents p
    """
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Atom) and self.name == other.name
    
    def __hash__(self):
        return hash(('Atom', self.name))
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def atoms(self):
        return {self.name}

class Not(Formula):
    """
    Logical negation.
 
    Example:
        Not(Atom('p')) represents ~p
    """
    def __init__(self, operand):
        self.operand = operand
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand
    
    def __hash__(self):
        return hash(('Not', self.operand))
    
    def __str__(self):
        if isinstance(self.operand, Atom):
            return f'~{self.operand}'
        return f'~({self.operand})'
    
    def __repr__(self):
        return f'Not({repr(self.operand)})'

    def atoms(self):
        return self.operand.atoms()

class And(Formula):
    """
    Logical conjunction (binary).

    Example:
        And(Atom('p'), Atom('q'))   represents   p ∧ q
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, And) and self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash(('And', self.left, self.right))
    
    def __str__(self):
        return f'({self.left} ∧ {self.right})'
    
    def __repr__(self):
        return f'And({repr(self.left)}, {repr(self.right)})'
    
    def atoms(self):
        return self.left.atoms() | self.right.atoms()

class Or(Formula):
    """
    Logical disjunction (binary).

    Example:
        Or(Atom('p'), Atom('q'))   represents   p ∨ q
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Or) and self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash(('Or', self.left, self.right))
    
    def __str__(self):
        return f'({self.left} ∨ {self.right})'
    
    def __repr__(self):
        return f'Or({repr(self.left)}, {repr(self.right)})'
    
    def atoms(self):
        return self.left.atoms() | self.right.atoms()

class Implies(Formula):
    """
    Logical implication (binary).

    Example:
        Implies(Atom('p'), Atom('q'))   represents   p → q
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Implies) and self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash(('Implies', self.left, self.right))
    
    def __str__(self):
        return f'({self.left} → {self.right})'
    
    def __repr__(self):
        return f'Implies({repr(self.left)}, {repr(self.right)})'
    
    def atoms(self):
        return self.left.atoms() | self.right.atoms()

class Biconditional(Formula):
    """
    Logical biconditional / if-and-only-if (binary).
 
    Example:
        Biconditional(Atom('p'), Atom('q'))   represents   (p ↔ q)
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Biconditional) and self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash(('Biconditional', self.left, self.right))
    
    def __str__(self):
        return f'({self.left} ↔ {self.right})'
    
    def __repr__(self):
        return f'Biconditional({repr(self.left)}, {repr(self.right)})'

    def atoms(self):
        return self.left.atoms() | self.right.atoms()