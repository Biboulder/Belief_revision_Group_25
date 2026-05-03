# Belief Revision - Group 25

## How to run

```bash
python agm_tests.py
```

## What it does

Given a belief base **B** and a new formula **φ**, produces a revised base **B \* φ** that:
- contains φ
- is consistent (when φ is consistent)
- keeps as much of the old beliefs as possible

## Files

- **`formula.py`** — Formula classes: `Atom`, `Not`, `And`, `Or`, `Implies`, `Biconditional`.
- **`parser.py`** — Parses strings like `"p -> (q & ~r)"` into formula trees.
- **`cnf.py`** — Converts formulas to CNF (eliminate `↔`, eliminate `→`, push `¬` inward, distribute `∨` over `∧`).
- **`resolution.py`** — Checks logical entailment via resolution refutation.
- **`belief_base.py`** — Stores formulas with priorities (insertion order = entrenchment).
- **`contraction.py`** — Partial meet contraction: removes least entrenched formulas until φ is gone.
- **`revision.py`** — Levi identity: `B * φ = (B − ¬φ) + φ`.
- **`agm_tests.py`** — Tests the 5 AGM postulates: Success, Inclusion, Vacuity, Consistency, Extensionality.
- **`main.py`** — Demo entry point.
