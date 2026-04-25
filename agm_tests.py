# Test all 5 AGM postulates
""" 
Success -> φ ∈ B * φ (the new belief is actually in the result)
Inclusion -> B * φ ⊆ B + φ (revision doesn't add unrelated stuff)
Vacuity -> If ¬φ ∉ B, then B * φ = B + φ (if no conflict, just expand)
Consistency -> B * φ is consistent, unless φ itself is a contradiction
Extensionality -> If φ ≡ ψ, then B * φ = B * ψ
 """


"""
agm_tests.py — AGM Postulate Tests for the Belief Revision Engine
Group 25, 02180 Intro to AI, SP25

Tests all 5 required AGM postulates:
  1. Success      — φ ∈ B * φ
  2. Inclusion    — B * φ ⊆ B + φ
  3. Vacuity      — If ¬φ ∉ Cn(B), then B * φ = B + φ
  4. Consistency  — B * φ is consistent, unless ⊢ ¬φ
  5. Extensionality — If ⊢ φ ↔ ψ, then B * φ = B * ψ

Run this file directly:
    python agm_tests.py

All tests use the same shared infrastructure (belief_base, revision, resolution).
Each test prints PASS / FAIL with a human-readable explanation.
"""

from formula import Atom, Not, And, Or, Implies, Biconditional
from belief_base import BeliefBase
from revision import revise
from resolution import is_entailed, is_consistent
from expansion import expand


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def formulas_entailed_by(bb: BeliefBase, formula_list):
    """Return which formulas from formula_list are entailed by bb."""
    base = bb.get_formulas()
    return [f for f in formula_list if is_entailed(base, f)]


def belief_bases_equivalent(bb1: BeliefBase, bb2: BeliefBase) -> bool:
    """
    Two belief bases are logically equivalent if each entails everything
    the other does — we check this by testing mutual entailment of their
    formulas (an approximation sufficient for finite bases).
    """
    f1 = bb1.get_formulas()
    f2 = bb2.get_formulas()
    # Every formula in bb2 is entailed by bb1 and vice-versa
    for f in f2:
        if not is_entailed(f1, f):
            return False
    for f in f1:
        if not is_entailed(f2, f):
            return False
    return True


def is_tautology(formula) -> bool:
    """
    A formula is a tautology if its negation is unsatisfiable,
    i.e., an empty belief base entails it.
    """
    return is_entailed([], formula)


def _report(name: str, passed: bool, detail: str = ""):
    status = "PASS ✓" if passed else "FAIL ✗"
    print(f"  [{status}] {name}" + (f": {detail}" if detail else ""))
    return passed


# ---------------------------------------------------------------------------
# Postulate 1 — Success
# ---------------------------------------------------------------------------
# After revising B by φ, φ must be in (entailed by) the resulting base.
# B * φ ⊨ φ
# ---------------------------------------------------------------------------

def test_success(bb: BeliefBase, formula, priority: int = 5) -> bool:
    """
    Success postulate: the revised belief base must entail the new formula.
    """
    revised = revise(bb, formula, priority)
    result = is_entailed(revised.get_formulas(), formula)
    return _report(
        "Success",
        result,
        f"Revised base {'does' if result else 'does NOT'} entail {formula}"
    )


# ---------------------------------------------------------------------------
# Postulate 2 — Inclusion
# ---------------------------------------------------------------------------
# Revision should not add beliefs that simple expansion wouldn't.
# B * φ ⊆ B + φ   (logically: everything in B*φ is also in B+φ)
# ---------------------------------------------------------------------------

def test_inclusion(bb: BeliefBase, formula, priority: int = 5) -> bool:
    """
    Inclusion postulate: every formula entailed by B*φ is also entailed by B+φ.
    """
    revised = revise(bb, formula, priority)
    expanded = expand(bb, formula, priority)

    revised_formulas = revised.get_formulas()
    expanded_formulas = expanded.get_formulas()

    # Check: everything the revised base entails individually,
    # the expanded base also entails
    violations = []
    for f in revised_formulas:
        if not is_entailed(expanded_formulas, f):
            violations.append(f)

    passed = len(violations) == 0
    return _report(
        "Inclusion",
        passed,
        f"{len(violations)} formula(s) in B*φ not entailed by B+φ" if not passed else "B*φ ⊆ B+φ holds"
    )


# ---------------------------------------------------------------------------
# Postulate 3 — Vacuity
# ---------------------------------------------------------------------------
# If the belief base does not entail ¬φ, then revision is the same as expansion.
# If ¬φ ∉ Cn(B), then B * φ = B + φ
# ---------------------------------------------------------------------------

def test_vacuity(bb: BeliefBase, formula, priority: int = 5) -> bool:
    """
    Vacuity postulate: if B does not entail ¬φ, revision equals expansion.
    """
    neg_formula = Not(formula)
    base_entails_neg = is_entailed(bb.get_formulas(), neg_formula)

    if base_entails_neg:
        # Vacuity doesn't apply — trivially pass with a note
        return _report(
            "Vacuity",
            True,
            "¬φ is already entailed by B — vacuity condition not triggered (trivially satisfied)"
        )

    revised = revise(bb, formula, priority)
    expanded = expand(bb, formula, priority)
    equivalent = belief_bases_equivalent(revised, expanded)

    return _report(
        "Vacuity",
        equivalent,
        "B*φ = B+φ (no conflict existed)" if equivalent else "B*φ ≠ B+φ despite ¬φ ∉ Cn(B)"
    )


# ---------------------------------------------------------------------------
# Postulate 4 — Consistency
# ---------------------------------------------------------------------------
# The revised belief base must be consistent, unless φ is itself a contradiction.
# B * φ is consistent, if φ is consistent.
# ---------------------------------------------------------------------------

def test_consistency(bb: BeliefBase, formula, priority: int = 5) -> bool:
    """
    Consistency postulate: B*φ is consistent as long as φ itself is consistent.
    """
    # Check if formula is consistent on its own
    formula_consistent = is_consistent([formula])

    if not formula_consistent:
        return _report(
            "Consistency",
            True,
            "φ is a contradiction — consistency postulate trivially satisfied"
        )

    revised = revise(bb, formula, priority)
    result_consistent = is_consistent(revised.get_formulas())

    return _report(
        "Consistency",
        result_consistent,
        "Revised base is consistent" if result_consistent else "Revised base is INCONSISTENT"
    )


# ---------------------------------------------------------------------------
# Postulate 5 — Extensionality
# ---------------------------------------------------------------------------
# Logically equivalent formulas produce the same revision.
# If ⊢ φ ↔ ψ, then B * φ = B * ψ
# ---------------------------------------------------------------------------

def test_extensionality(bb: BeliefBase, formula1, formula2, priority: int = 5) -> bool:
    """
    Extensionality postulate: if φ ≡ ψ (logically equivalent), then B*φ = B*ψ.
    """
    # Check if formula1 ↔ formula2 is a tautology
    biconditional = Biconditional(formula1, formula2)
    equivalent_formulas = is_tautology(biconditional)

    if not equivalent_formulas:
        return _report(
            "Extensionality",
            True,
            "φ and ψ are not logically equivalent — postulate not applicable (trivially satisfied)"
        )

    revised1 = revise(bb, formula1, priority)
    revised2 = revise(bb, formula2, priority)
    same_result = belief_bases_equivalent(revised1, revised2)

    return _report(
        "Extensionality",
        same_result,
        "B*φ = B*ψ for equivalent φ, ψ" if same_result else "B*φ ≠ B*ψ despite φ ≡ ψ"
    )


# ---------------------------------------------------------------------------
# run_all_tests — convenience wrapper
# ---------------------------------------------------------------------------

def run_all_tests(bb: BeliefBase, formula, priority: int = 5,
                  formula2=None, label: str = ""):
    """
    Run all 5 AGM postulate tests on a given belief base and revision formula.

    Args:
        bb:        the belief base to test
        formula:   the formula to revise by (φ)
        priority:  priority assigned to the new belief
        formula2:  a second formula logically equivalent to `formula`,
                   used for the Extensionality test. If None, we use
                   the double-negation ¬¬φ (always equivalent to φ).
        label:     optional label printed as a header
    """
    if label:
        print(f"\n{'='*60}")
        print(f"  Scenario: {label}")
        print(f"{'='*60}")

    if formula2 is None:
        formula2 = Not(Not(formula))   # ¬¬φ ≡ φ always

    results = [
        test_success(bb, formula, priority),
        test_inclusion(bb, formula, priority),
        test_vacuity(bb, formula, priority),
        test_consistency(bb, formula, priority),
        test_extensionality(bb, formula, formula2, priority),
    ]

    passed = sum(results)
    total = len(results)
    print(f"\n  Result: {passed}/{total} postulates satisfied\n")
    return passed == total


# ---------------------------------------------------------------------------
# Example test scenarios (run when executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  AGM Postulate Test Suite — Belief Revision Group 25")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Scenario 1 — Basic revision with no conflict
    # Belief base: {p, p → q}
    # Revise by: q
    # Expected: all 5 postulates pass; vacuity triggered (no conflict)
    # ------------------------------------------------------------------
    p = Atom('p')
    q = Atom('q')
    r = Atom('r')

    bb1 = BeliefBase()
    bb1.add(p, priority=3)
    bb1.add(Implies(p, q), priority=2)

    run_all_tests(bb1, q, priority=5, label="No conflict: B={p, p→q}, revise by q")

    # ------------------------------------------------------------------
    # Scenario 2 — Revision that forces removal of a belief
    # Belief base: {p, p → q}
    # Revise by: ¬p
    # Expected: p gets removed to restore consistency
    # ------------------------------------------------------------------
    bb2 = BeliefBase()
    bb2.add(p, priority=3)
    bb2.add(Implies(p, q), priority=2)

    run_all_tests(bb2, Not(p), priority=5, label="Conflict: B={p, p→q}, revise by ¬p")

    # ------------------------------------------------------------------
    # Scenario 3 — Revision by contradiction (⊥)
    # Belief base: {p}
    # Revise by: p ∧ ¬p
    # Consistency postulate is trivially satisfied (φ is a contradiction).
    # ------------------------------------------------------------------
    bb3 = BeliefBase()
    bb3.add(p, priority=3)

    contradiction = And(p, Not(p))
    run_all_tests(bb3, contradiction, priority=5,
                  label="Contradiction: B={p}, revise by p∧¬p")

    # ------------------------------------------------------------------
    # Scenario 4 — Extensionality with genuinely equivalent formulas
    # φ = p ∧ q
    # ψ = q ∧ p   (logically equivalent by commutativity of ∧)
    # Belief base: {r}
    # ------------------------------------------------------------------
    bb4 = BeliefBase()
    bb4.add(r, priority=2)

    phi = And(p, q)
    psi = And(q, p)
    run_all_tests(bb4, phi, priority=5, formula2=psi,
                  label="Extensionality: φ=p∧q, ψ=q∧p, B={r}")

    # ------------------------------------------------------------------
    # Scenario 5 — Richer belief base
    # B = {p, q, p→r, q→r}
    # Revise by: ¬r
    # Contraction must remove beliefs that entail r.
    # ------------------------------------------------------------------
    bb5 = BeliefBase()
    bb5.add(p, priority=4)
    bb5.add(q, priority=3)
    bb5.add(Implies(p, r), priority=2)
    bb5.add(Implies(q, r), priority=2)

    run_all_tests(bb5, Not(r), priority=5,
                  label="Rich base: B={p,q,p→r,q→r}, revise by ¬r")

    print("=" * 60)
    print("  All scenarios complete.")
    print("=" * 60)