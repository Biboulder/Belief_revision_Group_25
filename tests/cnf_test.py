import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from parser import Parser
from cnf import to_cnf
from formula import Atom, Not, And, Or, Implies, Biconditional

# Test 1: Eliminate Implication
print("Test 1: Eliminate Implication")
print("p -> q  should become  ¬p ∨ q  →  {{¬p, q}}")
cnf = to_cnf(Parser("p -> q").parse())
expected = {frozenset({Not(Atom('p')), Atom('q')})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 2: Eliminate Biconditional
print("Test 2: Eliminate Biconditional")
print("p <-> q  should become  (p -> q) ∧ (q -> p)  →  {{¬p, q}, {¬q, p}}")
cnf = to_cnf(Parser("p <-> q").parse())
expected = {
    frozenset({Not(Atom('p')), Atom('q')}),
    frozenset({Not(Atom('q')), Atom('p')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 3: Push Negation Inward - De Morgan's Law (AND)
print("Test 3: De Morgan's Law - Negation of AND")
print("~(p & q)  should become  ¬p ∨ ¬q  →  {{¬p, ¬q}}")
cnf = to_cnf(Parser("~(p & q)").parse())
expected = {frozenset({Not(Atom('p')), Not(Atom('q'))})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 4: Push Negation Inward - De Morgan's Law (OR)
print("Test 4: De Morgan's Law - Negation of OR")
print("~(p | q)  should become  ¬p ∧ ¬q  →  {{¬p}, {¬q}}")
cnf = to_cnf(Parser("~(p | q)").parse())
expected = {frozenset({Not(Atom('p'))}), frozenset({Not(Atom('q'))})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 5: Double Negation Elimination
print("Test 5: Double Negation Elimination")
print("~~p  should become  p  →  {{p}}")
cnf = to_cnf(Parser("~~p").parse())
expected = {frozenset({Atom('p')})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 6: Triple Negation
print("Test 6: Triple Negation")
print("~~~p  should become  ¬p  →  {{¬p}}")
cnf = to_cnf(Parser("~~~p").parse())
expected = {frozenset({Not(Atom('p'))})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 7: Distribute OR over AND
print("Test 7: Distribute OR over AND")
print("p | (q & r)  should become  (p ∨ q) ∧ (p ∨ r)  →  {{p, q}, {p, r}}")
cnf = to_cnf(Parser("p | (q & r)").parse())
expected = {
    frozenset({Atom('p'), Atom('q')}),
    frozenset({Atom('p'), Atom('r')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 8: Distribute OR over AND (reverse)
print("Test 8: Distribute OR over AND (reverse)")
print("(p & q) | r  should become  (p ∨ r) ∧ (q ∨ r)  →  {{p, r}, {q, r}}")
cnf = to_cnf(Parser("(p & q) | r").parse())
expected = {
    frozenset({Atom('p'), Atom('r')}),
    frozenset({Atom('q'), Atom('r')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 9: Simple AND (already in CNF)
print("Test 9: Simple AND (already in CNF)")
print("p & q  should stay  p ∧ q  →  {{p}, {q}}")
cnf = to_cnf(Parser("p & q").parse())
expected = {frozenset({Atom('p')}), frozenset({Atom('q')})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 10: Simple OR (already in CNF)
print("Test 10: Simple OR (already in CNF)")
print("p | q  should stay  p ∨ q  →  {{p, q}}")
cnf = to_cnf(Parser("p | q").parse())
expected = {frozenset({Atom('p'), Atom('q')})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 11: Single Atom
print("Test 11: Single Atom")
print("p  should stay  p  →  {{p}}")
cnf = to_cnf(Parser("p").parse())
expected = {frozenset({Atom('p')})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 12: Single Negated Atom
print("Test 12: Single Negated Atom")
print("~p  should stay  ¬p  →  {{¬p}}")
cnf = to_cnf(Parser("~p").parse())
expected = {frozenset({Not(Atom('p'))})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 13: Complex - Negated Implication
print("Test 13: Negated Implication")
print("~(p -> q)  should become  ~(¬p ∨ q) → p ∧ ¬q  →  {{p}, {¬q}}")
cnf = to_cnf(Parser("~(p -> q)").parse())
expected = {frozenset({Atom('p')}), frozenset({Not(Atom('q'))})}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 14: Complex - Negated Biconditional
print("Test 14: Negated Biconditional")
print("~(p <-> q)  should become  (p ∧ ¬q) ∨ (¬p ∧ q)  →  {{p, ¬p}, {p, q}, {¬q, ¬p}, {¬q, q}}")
cnf = to_cnf(Parser("~(p <-> q)").parse())
# ~(p <-> q) = ~((p -> q) & (q -> p)) = ~(p -> q) | ~(q -> p) = (p & ~q) | (~p & q)
# Distributing: {p, ~p}, {p, q}, {~q, ~p}, {~q, q}
expected = {
    frozenset({Atom('p'), Not(Atom('p'))}),
    frozenset({Atom('p'), Atom('q')}),
    frozenset({Not(Atom('q')), Not(Atom('p'))}),
    frozenset({Not(Atom('q')), Atom('q')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 15: Very Complex - Multiple operations
print("Test 15: Complex Formula")
print("(p -> q) & (q -> r)")
cnf = to_cnf(Parser("(p -> q) & (q -> r)").parse())
expected = {
    frozenset({Not(Atom('p')), Atom('q')}),
    frozenset({Not(Atom('q')), Atom('r')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 16: Nested Distribution
print("Test 16: Nested Distribution")
print("(p & q) | (r & s)  should distribute fully")
cnf = to_cnf(Parser("(p & q) | (r & s)").parse())
expected = {
    frozenset({Atom('p'), Atom('r')}),
    frozenset({Atom('p'), Atom('s')}),
    frozenset({Atom('q'), Atom('r')}),
    frozenset({Atom('q'), Atom('s')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")

# Test 17: Combination of all transformations
print("Test 17: Everything Combined")
print("~(p <-> q) | r")
cnf = to_cnf(Parser("~(p <-> q) | r").parse())
# From test 14, we know ~(p <-> q) gives 4 clauses
# Each needs to be ORed with r
expected = {
    frozenset({Atom('p'), Not(Atom('p')), Atom('r')}),
    frozenset({Atom('p'), Atom('q'), Atom('r')}),
    frozenset({Not(Atom('q')), Not(Atom('p')), Atom('r')}),
    frozenset({Not(Atom('q')), Atom('q'), Atom('r')})
}
assert cnf == expected, f"Expected {expected}, got {cnf}"
print("Passed\n")
print("ALL CNF TESTS PASSED!")