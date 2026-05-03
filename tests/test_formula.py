"""
Tests for formula.py — the propositional formula building blocks.
"""

import sys
import os
import unittest

# Allow running from the tests/ folder OR from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from formula import Atom, Not, And, Or, Implies, Biconditional


# ########## Shared fixtures used across all test classes #########################################
# -> saves some typing and makes tests more readable.

p = Atom('p')
q = Atom('q')
r = Atom('r')


# ########## 1. String representations ############################################################

class TestStringRepresentation(unittest.TestCase):
    """
    __str__ should produce clean, human-readable logical notation.
    __repr__ should produce a Python-style debug string.
    """

    def test_atom_str(self):
        self.assertEqual(str(Atom('p')), 'p')

    def test_not_str(self):
        self.assertEqual(str(Not(p)), '~p')

    def test_and_str(self):
        self.assertEqual(str(And(p, q)), '(p ∧ q)')

    def test_or_str(self):
        self.assertEqual(str(Or(p, q)), '(p ∨ q)')

    def test_implies_str(self):
        self.assertEqual(str(Implies(p, q)), '(p → q)')

    def test_biconditional_str(self):
        self.assertEqual(str(Biconditional(p, q)), '(p ↔ q)')


    def test_nested_str(self):
        # p → (q ∧ ~r)
        f = Implies(p, And(q, Not(r)))
        self.assertEqual(str(f), '(p → (q ∧ ~r))')

    def test_atom_repr(self):
        # Atom repr is just the name, which makes debugging easier.
        self.assertEqual(repr(Atom('p')), 'p')

    def test_not_repr(self):
        self.assertEqual(repr(Not(p)), 'Not(p)')

    def test_and_repr(self):
        self.assertEqual(repr(And(p, q)), 'And(p, q)')

    def test_implies_repr(self):
        self.assertEqual(repr(Implies(p, q)), 'Implies(p, q)')


# ########## 2. Equality ##########################################################################

class TestEquality(unittest.TestCase):
    """
    __eq__ checks structural equality — same type, same children.
    This is critical: resolution.py must be able to tell that two
    separately-constructed Atom('p') objects represent the same literal.
    """

    def test_atom_equal(self):
        self.assertEqual(Atom('p'), Atom('p'))

    def test_atom_not_equal_different_name(self):
        self.assertNotEqual(Atom('p'), Atom('q'))

    def test_not_equal(self):
        self.assertEqual(Not(p), Not(p))

    def test_not_not_equal(self):
        self.assertNotEqual(Not(p), Not(q))

    def test_and_equal(self):
        self.assertEqual(And(p, q), And(p, q))

    def test_and_order_matters(self):
        # And(p, q) <> And(q, p) — we preserve tree structure, not logical symmetry
        self.assertNotEqual(And(p, q), And(q, p))

    def test_or_equal(self):
        self.assertEqual(Or(p, q), Or(p, q))

    def test_implies_equal(self):
        self.assertEqual(Implies(p, q), Implies(p, q))

    def test_biconditional_equal(self):
        self.assertEqual(Biconditional(p, q), Biconditional(p, q))

    def test_different_types_not_equal(self):
        # Atom('p') vs Not(Atom('p')) — completely different
        self.assertNotEqual(Atom('p'), Not(Atom('p')))

    def test_atom_vs_and_not_equal(self):
        self.assertNotEqual(Atom('p'), And(p, q))

    def test_nested_equal(self):
        f1 = Implies(p, And(q, Not(r)))
        f2 = Implies(p, And(q, Not(r)))
        self.assertEqual(f1, f2)

    def test_nested_not_equal(self):
        f1 = Implies(p, And(q, Not(r)))
        f2 = Implies(p, And(r, Not(q)))   # swapped q and r inside
        self.assertNotEqual(f1, f2)


# ########## 3. Hashing (needed for sets and frozensets) #########################################

class TestHashing(unittest.TestCase):
    """
    __hash__ must be consistent with __eq__:
      if a == b  →  hash(a) == hash(b)

    This is what allows formulas to be stored in Python sets and frozensets,
    which cnf.py uses heavily (each CNF clause is a frozenset of literals).
    """

    def test_equal_atoms_same_hash(self):
        self.assertEqual(hash(Atom('p')), hash(Atom('p')))

    def test_equal_nots_same_hash(self):
        self.assertEqual(hash(Not(p)), hash(Not(p)))

    def test_atom_in_set(self):
        # Duplicate Atom('p') should collapse into one element
        s = {Atom('p'), Atom('p'), Atom('q')}
        self.assertEqual(len(s), 2)

    def test_formula_in_set_deduplication(self):
        # All distinct objects → set should have 3 elements, not 4
        s = {p, p, Not(p), And(p, q)}
        self.assertEqual(len(s), 3)

    def test_literal_in_frozenset(self):
        # cnf.py stores each clause as frozenset of literals
        clause = frozenset([Not(p), q])
        self.assertIn(Not(p), clause)
        self.assertIn(q, clause)
        self.assertNotIn(p, clause)       # ~p is in clause, but p is not

    def test_complementary_literals_both_storable(self):
        # Both p and ~p can live in the same frozenset (different hashes)
        clause = frozenset([p, Not(p)])
        self.assertEqual(len(clause), 2)

    def test_set_of_clauses(self):
        # resolution.py works with sets of frozensets (the full CNF)
        clause1 = frozenset([Not(p), q])
        clause2 = frozenset([p])
        cnf = {clause1, clause2}
        self.assertEqual(len(cnf), 2)
        self.assertIn(clause1, cnf)

    def test_formula_as_dict_key(self):
        # Belief base may use formulas as dict keys
        d = {p: 'high', Not(p): 'low'}
        self.assertEqual(d[Atom('p')], 'high')
        self.assertEqual(d[Not(Atom('p'))], 'low')


# ########## 4. atoms() — extract all propositional variable names ################################

class TestAtoms(unittest.TestCase):
    """
    atoms() recursively collects all variable names in a formula.
    Used by resolution.py to enumerate all variables for truth-table checks.

    NOTE: atoms() is declared in the base class but must be implemented
    in each subclass. If any test here fails with NotImplementedError,
    that subclass is missing its atoms() override.
    """

    def test_atom_atoms(self):
        self.assertEqual(Atom('p').atoms(), {'p'})

    def test_not_atoms(self):
        self.assertEqual(Not(p).atoms(), {'p'})

    def test_and_atoms(self):
        self.assertEqual(And(p, q).atoms(), {'p', 'q'})

    def test_or_atoms(self):
        self.assertEqual(Or(p, q).atoms(), {'p', 'q'})

    def test_implies_atoms(self):
        self.assertEqual(Implies(p, q).atoms(), {'p', 'q'})

    def test_biconditional_atoms(self):
        self.assertEqual(Biconditional(p, q).atoms(), {'p', 'q'})

    def test_nested_atoms(self):
        # p → (q ∧ ~r) uses p, q, r
        f = Implies(p, And(q, Not(r)))
        self.assertEqual(f.atoms(), {'p', 'q', 'r'})

    def test_repeated_variable(self):
        # (p ∧ p) still gives just {'p'} — it's a set, not a list
        f = And(p, p)
        self.assertEqual(f.atoms(), {'p'})


# ########## 5. Entry point #######################################################################

if __name__ == '__main__':
    unittest.main(verbosity=2)