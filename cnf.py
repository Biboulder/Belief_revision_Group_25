# CNF conversion
# A mechanical process in 5 steps:
# - Eliminate ↔ (biconditionals)
# - Eliminate → (implications)
# - Push ¬ inward (De Morgan's laws)
# - Eliminate double negations
# - Distribute ∨ over ∧



from formula import Formula, Atom, Not, And, Or, Implies, Biconditional

def eliminate_biconditional(f):
    if isinstance(f, Atom):
        return f
    if isinstance(f, Not):
        return Not(eliminate_biconditional(f.operand))
    if isinstance(f, And):
        return And(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Or):
        return Or(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Implies):
        return Implies(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Biconditional):
        l = eliminate_biconditional(f.left)
        r = eliminate_biconditional(f.right)
        return And(Implies(l, r), Implies(r, l))

def eliminate_implication(f):
    if isinstance(f, Atom):
        return f
    if isinstance(f, Not):
        return Not(eliminate_implication(f.operand))
    if isinstance(f, And):
        return And(eliminate_implication(f.left), eliminate_implication(f.right))
    if isinstance(f, Or):
        return Or(eliminate_implication(f.left), eliminate_implication(f.right))
    if isinstance(f, Implies):
        return Or(Not(eliminate_implication(f.left)), eliminate_implication(f.right))

def push_negation_inward(f):
    if isinstance(f, Atom):
        return f
    if isinstance(f, Not):
        inner = f.operand
        if isinstance(inner, Atom):
            return f
        if isinstance(inner, Not):
            return push_negation_inward(inner.operand)
        if isinstance(inner, And):
            return Or(push_negation_inward(Not(inner.left)),
                      push_negation_inward(Not(inner.right)))
        if isinstance(inner, Or):
            return And(push_negation_inward(Not(inner.left)),
                       push_negation_inward(Not(inner.right)))
    if isinstance(f, And):
        return And(push_negation_inward(f.left), push_negation_inward(f.right))
    if isinstance(f, Or):
        return Or(push_negation_inward(f.left), push_negation_inward(f.right))

def distribute_or_over_and(f):
    if isinstance(f, Atom) or isinstance(f, Not):
        return f
    if isinstance(f, And):
        return And(distribute_or_over_and(f.left), distribute_or_over_and(f.right))
    if isinstance(f, Or):
        left = distribute_or_over_and(f.left)
        right = distribute_or_over_and(f.right)
        if isinstance(left, And):
            return And(distribute_or_over_and(Or(left.left, right)),
                       distribute_or_over_and(Or(left.right, right)))
        if isinstance(right, And):
            return And(distribute_or_over_and(Or(left, right.left)),
                       distribute_or_over_and(Or(left, right.right)))
        return Or(left, right)

def collect_clauses(f):
    """Convert an And-tree into a set of frozensets (each = one clause)."""
    if isinstance(f, And):
        return collect_clauses(f.left) | collect_clauses(f.right)
    else:
        return {collect_literals(f)}

def collect_literals(f):
    """Convert an Or-tree into a frozenset of literals."""
    if isinstance(f, Or):
        return collect_literals(f.left) | collect_literals(f.right)
    else:
        return frozenset([f])

def to_cnf(formula):
    """Return a set of frozensets representing the CNF of formula."""
    f = eliminate_biconditional(formula)
    f = eliminate_implication(f)
    f = push_negation_inward(f)
    f = distribute_or_over_and(f)
    return collect_clauses(f)