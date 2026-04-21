# Belief_revision_Group_25

## `formula.py` — The Building Blocks

This is your data layer. Every formula in the system is represented as a **tree of objects**.

**What it contains:**
- A base class `Formula`
- Subclasses: `Atom`, `Not`, `And`, `Or`, `Implies`, `Biconditional`
- Each class needs:
  - `__init__` to store its children (e.g. `And` stores `left` and `right`)
  - `__repr__` or `__str__` so you can print formulas nicely
  - `__eq__` and `__hash__` so formulas can be compared and stored in sets

**Example of what it enables:**
```python
f = Implies(Atom('p'), And(Atom('q'), Not(Atom('r'))))
# represents: p → (q ∧ ¬r)
```

---

## `cnf.py` — Formula Normalisation

Takes any formula and converts it to **Conjunctive Normal Form** — a set of clauses, where each clause is a set of literals.

**What it contains:**
- `eliminate_biconditional(formula)` — replaces `A ↔ B` with `(A → B) ∧ (B → A)`
- `eliminate_implication(formula)` — replaces `A → B` with `¬A ∨ B`
- `push_negation_inward(formula)` — applies De Morgan's laws
- `eliminate_double_negation(formula)` — replaces `¬¬A` with `A`
- `distribute_or_over_and(formula)` — flattens into CNF structure
- `to_cnf(formula)` — calls all of the above in order and returns a set of frozensets (clauses of literals)

**Example of what it produces:**
```python
to_cnf(Implies(Atom('p'), Atom('q')))
# → { frozenset({Not(Atom('p')), Atom('q')}) }
# i.e. the single clause: {¬p, q}
```

---

## `resolution.py` — Logical Entailment

Uses the CNF clauses to check whether a formula logically follows from a set of formulas.

**What it contains:**
- `resolve(clause1, clause2)` — tries to combine two clauses by cancelling a literal and its negation, returns the resulting clause or `None`
- `is_entailed(kb, formula)` — the main function:
  1. Negates `formula`
  2. Converts `kb ∪ {¬formula}` to CNF clauses
  3. Repeatedly applies `resolve` on all clause pairs
  4. Returns `True` if the empty clause is derived, `False` otherwise
- `is_consistent(formulas)` — checks whether a set of formulas has no contradiction (used in contraction)

**Example of what it enables:**
```python
kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
is_entailed(kb, Atom('q'))  # → True
```

---

## `belief_base.py` — Storage of Beliefs

A simple data structure that stores formulas together with their priorities.

**What it contains:**
- A `BeliefBase` class with an internal list of `(formula, priority)` pairs
- `add(formula, priority)` — adds a belief
- `remove(formula)` — removes a specific belief
- `get_formulas()` — returns just the formulas (for passing to resolution)
- `get_sorted()` — returns beliefs sorted by priority, highest first
- `__str__` — prints the belief base in a readable way

**Example:**
```python
bb = BeliefBase()
bb.add(Atom('p'), priority=3)
bb.add(Implies(Atom('p'), Atom('q')), priority=2)
bb.add(Atom('q'), priority=1)
```

---

## `contraction.py` — Removing a Belief

Implements **partial meet contraction**: shrink the belief base so it no longer entails φ, while losing as little as possible.

**What it contains:**
- `get_remainders(belief_base, formula)` — finds all maximal subsets of the belief base that do **not** entail `formula`. These are the "remainders"
- `selection_function(remainders, belief_base)` — picks the best remainders using the priority order (prefer subsets that retain high-priority formulas)
- `contract(belief_base, formula)` — calls the above two, takes the intersection of selected remainders, returns the new `BeliefBase`

**How the selection function uses priority:**
```python
# Score a remainder by summing the priorities of formulas it keeps
score = sum(priority for f, priority in belief_base if f in remainder)
# Pick the remainder(s) with the highest score
```

---

## `revision.py` — The Levi Identity

Combines contraction and expansion to perform full belief revision.

**What it contains:**
- `expand(belief_base, formula, priority)` — simply adds `formula` to the belief base at the given priority
- `revise(belief_base, formula, priority)` — implements the Levi identity:
  1. Contract `¬formula` from the belief base
  2. Expand with `formula`

```python
def revise(belief_base, formula, priority):
    contracted = contract(belief_base, Not(formula))
    return expand(contracted, formula, priority)
```

---

## `agm_tests.py` — Verifying Correctness

Tests all 5 required AGM postulates against your revision engine.

**What it contains, one test per postulate:**
- `test_success(bb, formula)` — after revision, `formula` must be in the result
- `test_inclusion(bb, formula)` — result must be a subset of simply expanding with `formula`
- `test_vacuity(bb, formula)` — if `¬formula` wasn't in `bb`, revision = expansion
- `test_consistency(bb, formula)` — result must be consistent (unless `formula` is a contradiction)
- `test_extensionality(bb, f1, f2)` — if `f1 ≡ f2`, revising by either gives the same result

---

## `main.py` — Demo / Entry Point

Wires everything together and shows the engine working end to end.

**What it contains:**
- A hardcoded or interactive example belief base
- A sequence of revision operations
- Printed output showing the belief base before and after each operation
- Calls to `agm_tests.py` to confirm correctness