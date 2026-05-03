# Belief Revision - Group 25
A belief revision engine for propositional logic, implemented in Python from scratch.

## How to run

```bash
python main.py
```
 
To run only the AGM postulate tests: 
```bash
python agm_tests.py
```
 
Both should report **5/5 postulates satisfied** in each of the five test scenarios.

### Unit tests
 
The `tests/` folder contains lower-level tests for individual modules:
 
```bash
python tests/test_formula.py      # 40 unit test cases for the formula classes
python tests/cnf_test.py          # 17 assertion tests for CNF conversion
python tests/parser_test.py       # parser tests
```

---
 
## Project structure
The code is organised in three layers, mirroring the report:
### Data layer
- **`formula.py`** — Propositional formula classes: `Atom`, `Not`, `And`, `Or`, `Implies`, `Biconditional`. Each implements `__eq__`, `__hash__`, and `__str__` so formulas can be used as dictionary/set keys and printed readably.
- **`parser.py`** — Recursive-descent parser converting strings such as `"p -> (q & ~r)"` into formula trees. Operator syntax: `~` (not), `&` (and), `|` (or), `->` (implies, right-associative), `<->` (biconditional, left-associative).
- **`belief_base.py`** — `BeliefBase` class storing formulas in insertion order. Index 0 is the most entrenched (added first). Exposes `add`, `remove`, `get_formulas`, `get_sorted`.
### Logical layer
- **`cnf.py`** — Conversion to Conjunctive Normal Form via the standard pipeline: eliminate `↔`, eliminate `→`, push `¬` inward (De Morgan + double-negation), distribute `∨` over `∧`. Output is a set of frozensets of literals (one frozenset per clause).
- **`resolution.py`** — `is_entailed(B, φ)` and `is_consistent(B)` via resolution refutation. Iteratively pairs clauses, terminates when the empty clause is derived (entailment / inconsistency) or no new clauses are produced.
### Belief-revision layer
- **`contraction.py`** — Partial-meet contraction `B ÷ φ`: enumerate maximal subsets that don't entail `φ` (the remainders), score them by summed entrenchment, intersect the highest-scoring ones. Handles two edge cases: if `B ⊭ φ` returns `B` unchanged; if `φ` is a tautology returns the empty base.
- **`expansion.py`** — `B + φ = B ∪ {φ}`. No consistency check (revision handles that).
- **`revision.py`** — `B * φ = (B ÷ ¬φ) + φ` (Levi identity).
### Tests & demo
- **`agm_tests.py`** — End-to-end tests for the five AGM postulates (Success, Inclusion, Vacuity, Consistency, Extensionality) across five scenarios.
- **`main.py`** — Demo walking through stages 1–5 from the assignment brief, then runs the postulate test suite.
- **`tests/`** — Unit tests for individual building blocks:
  - `tests/test_formula.py` — 40 unittest cases for the formula classes (string representation, equality, hashing, atoms).
  - `tests/cnf_test.py` — 17 assertion-based tests for the CNF pipeline (implication/biconditional elimination, De Morgan, double negation, distribution).
  - `tests/parser_test.py` — Parser smoke tests printing parsed trees for a range of inputs.
