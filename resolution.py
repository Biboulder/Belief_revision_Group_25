# Entailment checking via resolution 
# - Convert formulas to CNF (Conjunctive Normal Form) (cnf.py)
# - Apply the resolution rule repeatedly (resolution.py)
# - If you derive False (empty clause), the set is unsatisfiable 

# Negate φ, convert to CNF
# Add to B's clauses
# Repeatedly apply resolution
# If you derive the empty clause → entailment holds ✓



from formula import Atom, Not
from cnf import to_cnf

def negate_literal(lit):
    if isinstance(lit, Not):
        return lit.operand
    return Not(lit)

def resolve(clause1, clause2):
    """Try to resolve two clauses. Returns set of new clauses produced."""
    new_clauses = set()
    for lit in clause1:
        neg = negate_literal(lit)
        if neg in clause2:
            resolvent = (clause1 - {lit}) | (clause2 - {neg})
            new_clauses.add(frozenset(resolvent))
    return new_clauses

def is_entailed(kb_formulas, formula):
    """Return True if kb_formulas logically entails formula."""
    # Refutation: add ¬formula, try to derive empty clause
    clauses = set()
    for f in kb_formulas:
        clauses |= to_cnf(f)
    clauses |= to_cnf(Not(formula))

    while True:
        new = set()
        clause_list = list(clauses)
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                resolvents = resolve(clause_list[i], clause_list[j])
                if frozenset() in resolvents:
                    return True   # empty clause derived → entailed
                new |= resolvents
        if new.issubset(clauses):
            return False          # no new clauses → not entailed
        clauses |= new

def is_consistent(formulas):
    """Return True if the set of formulas is consistent (has no contradiction)."""
    clauses = set()
    for f in formulas:
        clauses |= to_cnf(f)

    while True:
        new = set()
        clause_list = list(clauses)
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                resolvents = resolve(clause_list[i], clause_list[j])
                if frozenset() in resolvents:
                    return False  # contradiction found
                new |= resolvents
        if new.issubset(clauses):
            return True           # no contradiction possible
        clauses |= new