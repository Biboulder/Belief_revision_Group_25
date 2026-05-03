# 02180 Intro to AI — Belief Revision Engine (Group 25)

## Project context
Belief revision engine for the **02180 Intro to AI** course assignment (due **2026-05-04**). The agent maintains a propositional belief base and revises it when given a new formula, using the AGM framework (Levi identity, partial meet contraction, resolution-based entailment).

The project follows **Option A** from the assignment brief (standard belief base over formulas), **not** Option B (plausibility orders over possible worlds). Don't add a worlds-based revision path unless the user explicitly asks.

Language: **Python 3** (no `requirements.txt` — stdlib only).

## Hard constraints (do not violate)
- **No external logic libraries.** No Z3, SymPy, PySAT, `sympy.logic`, `aima-python`, etc. Resolution and CNF conversion are implemented from scratch in [cnf.py](cnf.py) and [resolution.py](resolution.py). Stdlib (`itertools`, `unittest`) is fine.
- **Symbolic input only.** Formulas are constructed by composing the classes in [formula.py](formula.py) — no parser, no natural language. Don't add a string-parser unless asked.
- **AGM postulates are the test oracle.** Success, Inclusion, Vacuity, Consistency, Extensionality (see [agm_tests.py](agm_tests.py)). Any change to revision/contraction/expansion semantics must keep all five passing across the existing scenarios.
- **Mathematical naming.** Identifiers and comments should mirror the course terminology (`remainders`, `selection_function`, `is_entailed`, `Levi identity`, `partial meet`, etc.). When adding code, reference the formal step it implements in a short comment.

## Repository layout
```
formula.py        Formula AST: Atom, Not, And, Or, Implies, Biconditional
cnf.py            CNF conversion → set of frozensets (each clause = frozenset of literals)
resolution.py     is_entailed(kb, φ) and is_consistent(formulas) via refutation resolution
belief_base.py    BeliefBase: ordered list, insertion order encodes entrenchment
contraction.py    Partial meet contraction (B ÷ φ): remainders + priority-weighted selection
expansion.py      Expansion (B + φ): append if absent
revision.py       revise(B, φ) = (B ÷ ¬φ) + φ   (Levi identity)
agm_tests.py      Hand-rolled AGM postulate test suite + demo scenarios
main.py           Entry-point stub (currently just a comment)
tests/
  test_formula.py unittest tests for the Formula AST
README.md         Per-file walkthrough (slightly stale — see "Known doc drift" below)
```

## Running things
- Run the AGM postulate suite (this is the main demo): `python agm_tests.py`
- Run the AST unit tests: `python -m unittest tests.test_formula` or `python tests/test_formula.py`
- `python main.py` currently does nothing — it's a placeholder. If asked to "run the project", run `agm_tests.py` instead, or extend `main.py` to wire up a demo (the user has not asked for this yet).
- There is no `pytest` configuration. Tests use stdlib `unittest`. Don't introduce pytest unless the user asks.

## Key design decisions already made
- **Entrenchment is insertion order.** [belief_base.py](belief_base.py) stores beliefs in a list; index 0 is most entrenched. `BeliefBase.add(formula)` is single-argument — there is **no `priority=` parameter**. `get_sorted()` derives a numeric priority `len(beliefs) - i` on the fly for the selection function. (The README still shows a `priority=` kwarg in some examples — that's stale.)
- **CNF clauses are `set[frozenset[Formula]]`.** A clause is a `frozenset` of literals (where a literal is an `Atom` or `Not(Atom)`). The full CNF is a `set` of such clauses. This relies on `__hash__`/`__eq__` on every `Formula` subclass — don't break those.
- **Negation pushing folds in double-negation elimination.** [cnf.py](cnf.py) does *not* have a separate `eliminate_double_negation` step; the `Not(Not(x))` case is handled inside `push_negation_inward` (line ~48). The README lists it as a separate step — that's stale.
- **Resolution loop is naive O(n²) per round.** [resolution.py](resolution.py) iterates all clause pairs each pass and stops when no new clauses are produced. Fine for the small bases used in tests; don't be surprised if a large input is slow. Don't add subsumption/indexing unless the user asks.
- **Selection function = priority-sum.** [contraction.py](contraction.py) `selection_function` scores each remainder by summing the (insertion-order-derived) priorities of the formulas it keeps, and picks the maximum. Then `contract` takes the **intersection** of all top-scoring remainders.
- **`revise(bb, φ)` takes two arguments**, not three. There's no priority argument on revision/expansion. (The README example showing `revise(bb, formula, priority)` is stale.)

## Known doc drift
[README.md](README.md) was written against an earlier API and has small inaccuracies — when the user asks about behavior, trust the code, not the README:
- It shows `bb.add(Atom('p'), priority=3)` — actual API is `bb.add(formula)` only.
- It lists `eliminate_double_negation` as a separate CNF step — it's folded into `push_negation_inward`.
- It shows `revise(bb, formula, priority)` — actual signature is `revise(belief_base, formula)`.

If the user asks to update the README, fix these. Otherwise leave it alone.

## When extending the engine
- New formula connectives → add a class in [formula.py](formula.py) with `__eq__`, `__hash__`, `__str__`, `__repr__`, `atoms()`, **and** add cases to every recursive function in [cnf.py](cnf.py) (`eliminate_biconditional`, `eliminate_implication`, `push_negation_inward`, `distribute_or_over_and`). Missing a case in any of those functions silently returns `None` and breaks resolution downstream.
- New AGM postulate test → add a `test_<name>(bb, formula)` in [agm_tests.py](agm_tests.py) following the `_report` pattern, and include it in `run_all_tests`.
- Belief-base reorganisation (e.g. moving away from insertion-order entrenchment to explicit priorities) is a real change with downstream effects in `contraction.selection_function` and the `BeliefBase.add` callers in `agm_tests.py` — flag it and confirm with the user before doing it.

## Mastermind extension
Optional per the brief, **not started**. If the user asks to begin it, the belief base should encode the game rules + the first guess; revision happens on each feedback. Don't scaffold this preemptively.

## Deliverables (for reference, not your job to produce unprompted)
1. Source code zip + README with run instructions.
2. Report PDF, 4–6 pages (7 if Mastermind), structured to match the assignment's stage list.
3. Division-of-labour PDF (max 4 students).

## Tone for code suggestions
- Short comments that name the formal step ("Levi identity", "partial meet — intersection of selected remainders", "refutation: add ¬φ and resolve to ⊥").
- No defensive boilerplate or speculative abstractions — the code is small and read by graders.
- Match the existing style: single-letter math-ish locals (`f`, `p`, `q`, `bb`) are fine in this codebase.
