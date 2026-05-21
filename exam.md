# Exam Exercise Guide — Belief Revision Group 25

This file contains one example question for every exercise type that appears in
past exams (2021, 2022, 2026 practice) AND is covered by this repo + the
`exam_utils.py` additions.

For each exercise you will find:
- The example question (exactly as it could appear on the exam)
- What to change in the code to solve it
- How to run it
- What to expect in the output

---

## Exercise Type 1 — Compute the remainder set A÷φ

### Example question

> Consider the belief base `A = {p, q, p∧q, p∨q}`.
> Which of the following sets are elements of `A ÷ p`?
>
> - `{q}`
> - `{q, p∨q}`
> - `{p, q}`
> - `{q, p∧q}`
> - `{p∧q, p∨q}`

### What to change

```python
from exam_utils import run_exam_exercise

run_exam_exercise(
    label="Type 1: A = {p, q, p&q, p|q}, compute A÷p",
    base_formulas=["p", "q", "p & q", "p | q"],
    contract_formula="p",
    check_remainder_candidates=[
        ["q"],
        ["q", "p | q"],
        ["p", "q"],
        ["q", "p & q"],
        ["p & q", "p | q"],
    ]
)
```

### How to run

```bash
python3 main.py
```

### Expected output
```
Remainder set:
  A ÷ p  —  1 remainder(s):
  [0] {q, (p ∨ q)}

Candidate membership:
  {q} ∈ A ÷ p ?  False
  {q, (p ∨ q)} ∈ A ÷ p ?  True
  {p, q} ∈ A ÷ p ?  False
  {q, (p ∧ q)} ∈ A ÷ p ?  False
  {(p ∧ q), (p ∨ q)} ∈ A ÷ p ?  False
```

Note: formulas are displayed using their internal string representation —
`p & q` becomes `(p ∧ q)`, `p | q` becomes `(p ∨ q)`, `p -> q` becomes `(p → q)`.

---

## Exercise Type 2 — Contract the belief base by φ

### Example question

> `B = {p, p→q, q→r}` (added in this order, so `p` is most entrenched).
> What is `B ÷ r`? Does it still entail `r`?

### What to change

```python
run_exam_exercise(
    label="Type 2: B = {p, p->q, q->r}, contract by r",
    base_formulas=["p", "p -> q", "q -> r"],
    contract_formula="r",
    check_formulas=["r", "q", "p"]
)
```

### Expected output
```
After contraction by r:
  e=2  p
  e=1  (p → q)

Entailment check on result:
  B |= r ?  False
  B |= q ?  True
  B |= p ?  True
```

The contracted base is `{p, p→q}`. `p` and `p→q` together entail `q` (modus ponens),
so `B |= q` is `True`. Only `r` is removed from the consequence set.

---

## Exercise Type 3 — Revise the belief base by φ (Levi identity)

### Example question

> `B = {p, p→q}`. What is `B * ¬p`?
> Does the result entail `q`? Does it entail `¬p`? Is it consistent?

### What to change

```python
run_exam_exercise(
    label="Type 3: B = {p, p->q}, revise by ~p",
    base_formulas=["p", "p -> q"],
    revise_formula="~p",
    check_formulas=["p", "~p", "q", "p -> q"]
)
```

### Expected output
```
After revision by ~p:
  e=2  (p → q)
  e=1  ~p

Entailment check on result:
  B |= p ?  False
  B |= ~p ?  True
  B |= q ?  False
  B |= (p → q) ?  True
```

`p→q` is retained (it was more entrenched than `p`). `q` is no longer entailed because
`p` was removed and `¬p` was added — `¬p` and `p→q` do not together entail `q`.

---

## Exercise Type 4 — Yes/No membership table for B*φ

This is the most common exam format: a list of formulas, answer True/False each.

### Example question

> `B = {p, q, p→q}`. Revise by `¬q`.
> For each formula decide if it is in `B * ¬q`:
> `p`, `q`, `¬q`, `p∧q`, `p∨q`, `p→q`

### What to change

```python
run_exam_exercise(
    label="Type 4: B = {p, q, p->q}, revise by ~q — membership table",
    base_formulas=["p", "q", "p -> q"],
    revise_formula="~q",
    check_formulas=["p", "q", "~q", "p & q", "p | q", "p -> q"]
)
```

### Expected output — read these as your Yes/No column
```
Entailment check on result:
  B |= p ?  True
  B |= q ?  False
  B |= ~q ?  True
  B |= (p ∧ q) ?  False
  B |= (p ∨ q) ?  True
  B |= (p → q) ?  False
```

---

## Exercise Type 5 — AGM postulate verification

### Example question

> `B = {p, q, p→r, q→r}`. Revise by `¬r`.
> Does the result satisfy the AGM postulates? Check: Success, Consistency, Vacuity.

### What to change

This is already in `main.py` as `bb5`. Just run:

```bash
python3 main.py
```

And look for:
```
Scenario: Rich base: B={p,q,p→r,q→r}, revise by ¬r
```

To add your own AGM check:

```python
from formula import Atom, Not, Implies
from belief_base import BeliefBase
import agm_tests

p, q, r = Atom('p'), Atom('q'), Atom('r')
bb = BeliefBase()
bb.add(p); bb.add(q); bb.add(Implies(p, r)); bb.add(Implies(q, r))
agm_tests.run_all_tests(bb, Not(r), label="My scenario")
```

### Expected output

```
[PASS ✓] Success
[PASS ✓] Inclusion
[PASS ✓] Vacuity
[PASS ✓] Consistency
[PASS ✓] Extensionality

  Result: 5/5 postulates satisfied
```

---

## Exercise Type 6 — Entailment checks: does B |= φ?

### Example question

> `B = {p, p→q}`. Decide for each: does `B |= φ`?
> - `q`, `r`, `p∧q`, `¬p`

### What to change

```python
run_exam_exercise(
    label="Type 6: B = {p, p->q}, entailment checks",
    base_formulas=["p", "p -> q"],
    check_formulas=["q", "r", "p & q", "~p"]
)
```

### Expected output
```
Entailment check on result:
  B |= q ?  True
  B |= r ?  False
  B |= (p ∧ q) ?  True
  B |= ~p ?  False
```

---

## Exercise Type 7 — Expansion B+φ

### Example question

> `B = {p, p→q}`. What is `B + r`? Is it consistent?

### What to change

Expansion is not in `run_exam_exercise`, call it directly:

```python
from belief_base import BeliefBase
from expansion import expand
from resolution import is_entailed, is_consistent
from parser import Parser

def p(s): return Parser(s).parse()

bb = BeliefBase()
bb.add(p("p")); bb.add(p("p -> q"))
expanded = expand(bb, p("r"))

print("B + r:")
for f in expanded.get_formulas():
    print(f"  {f}")
print(f"B+r |= r          ?  {is_entailed(expanded.get_formulas(), p('r'))}")
print(f"B+r is consistent ?  {is_consistent(expanded.get_formulas())}")
```

### Expected output
```
B + r:
  p
  (p → q)
  r
B+r |= r          ?  True
B+r is consistent ?  True
```

---

## Quick-reference: formula syntax

| Math notation | Type in code |
|---|---|
| p ∧ q | `"p & q"` |
| p ∨ q | `"p \| q"` |
| ¬p | `"~p"` |
| p → q | `"p -> q"` |
| p ↔ q | `"p <-> q"` |

---

## Quick-reference: which function for which goal

| Goal | Function |
|---|---|
| Compute and print all remainders `A÷φ` | `show_remainders(bb, formula)` |
| Check if candidate subsets are remainders | `check_remainder_membership(bb, formula, candidates)` |
| Contract `B` by `φ` | `contract(bb, formula)` |
| Revise `B` by `φ` | `revise(bb, formula)` |
| Expand `B` by `φ` | `expand(bb, formula)` |
| Check `B |= φ` for a list | `check_entailment_list(bb, ["p", "q", ...])` |
| Check consistency | `is_consistent(bb.get_formulas())` |
| Run all AGM postulate tests | `agm_tests.run_all_tests(bb, formula)` |
| Solve a full exam exercise in one call | `run_exam_exercise(label, base_formulas, ...)` |
