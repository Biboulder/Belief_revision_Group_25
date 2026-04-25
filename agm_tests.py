# Test all 5 AGM postulates
""" 
Success -> φ ∈ B * φ (the new belief is actually in the result)
Inclusion -> B * φ ⊆ B + φ (revision doesn't add unrelated stuff)
Vacuity -> If ¬φ ∉ B, then B * φ = B + φ (if no conflict, just expand)
Consistency -> B * φ is consistent, unless φ itself is a contradiction
Extensionality -> If φ ≡ ψ, then B * φ = B * ψ
 """


from formula import Atom, Not, And, Or, Implies, Biconditional
from belief_base import BeliefBase
from revision import revise
from resolution import is_entailed, is_consistent
from expansion import expand


def is_tautology(formula):
    return is_entailed([], formula)

def belief_bases_equivalent(bb1, bb2):
    f1 = bb1.get_formulas()
    f2 = bb2.get_formulas()
    for f in f2:
        if not is_entailed(f1, f):
            return False
    for f in f1:
        if not is_entailed(f2, f):
            return False
    return True

def _report(name, passed, detail=""):
    status = "PASS ✓" if passed else "FAIL ✗"
    print(f"  [{status}] {name}" + (f": {detail}" if detail else ""))
    return passed


def test_success(bb, formula):
    revised = revise(bb, formula)
    result = is_entailed(revised.get_formulas(), formula)
    return _report("Success", result)

def test_inclusion(bb, formula):
    revised = revise(bb, formula)
    expanded = expand(bb, formula)
    violations = [f for f in revised.get_formulas()
                  if not is_entailed(expanded.get_formulas(), f)]
    return _report("Inclusion", len(violations) == 0)

def test_vacuity(bb, formula):
    if is_entailed(bb.get_formulas(), Not(formula)):
        return _report("Vacuity", True, "¬φ entailed — condition not triggered")
    revised = revise(bb, formula)
    expanded = expand(bb, formula)
    return _report("Vacuity", belief_bases_equivalent(revised, expanded))

def test_consistency(bb, formula):
    if not is_consistent([formula]):
        return _report("Consistency", True, "φ is a contradiction — trivially satisfied")
    revised = revise(bb, formula)
    return _report("Consistency", is_consistent(revised.get_formulas()))

def test_extensionality(bb, formula1, formula2):
    if not is_tautology(Biconditional(formula1, formula2)):
        return _report("Extensionality", True, "φ and ψ not equivalent — not applicable")
    revised1 = revise(bb, formula1)
    revised2 = revise(bb, formula2)
    return _report("Extensionality", belief_bases_equivalent(revised1, revised2))


def run_all_tests(bb, formula, formula2=None, label=""):
    if label:
        print(f"\n{'='*60}")
        print(f"  Scenario: {label}")
        print(f"{'='*60}")
    if formula2 is None:
        formula2 = Not(Not(formula))
    results = [
        test_success(bb, formula),
        test_inclusion(bb, formula),
        test_vacuity(bb, formula),
        test_consistency(bb, formula),
        test_extensionality(bb, formula, formula2),
    ]
    print(f"\n  Result: {sum(results)}/{len(results)} postulates satisfied\n")
    return all(results)


if __name__ == "__main__":
    print("=" * 60)
    print("  AGM Postulate Test Suite — Belief Revision Group 25")
    print("=" * 60)

    p = Atom('p')
    q = Atom('q')
    r = Atom('r')

    # Scenario 1 — No conflict
    bb1 = BeliefBase()
    bb1.add(p)
    bb1.add(Implies(p, q))
    run_all_tests(bb1, q, label="No conflict: B={p, p→q}, revise by q")

    # Scenario 2 — Direct conflict
    bb2 = BeliefBase()
    bb2.add(p)
    bb2.add(Implies(p, q))
    run_all_tests(bb2, Not(p), label="Conflict: B={p, p→q}, revise by ¬p")

    # Scenario 3 — Contradiction as input
    bb3 = BeliefBase()
    bb3.add(p)
    run_all_tests(bb3, And(p, Not(p)), label="Contradiction: B={p}, revise by p∧¬p")

    # Scenario 4 — Extensionality
    bb4 = BeliefBase()
    bb4.add(r)
    run_all_tests(bb4, And(p, q), formula2=And(q, p), label="Extensionality: φ=p∧q, ψ=q∧p")

    # Scenario 5 — Richer base
    bb5 = BeliefBase()
    bb5.add(p)
    bb5.add(q)
    bb5.add(Implies(p, r))
    bb5.add(Implies(q, r))
    run_all_tests(bb5, Not(r), label="Rich base: B={p,q,p→r,q→r}, revise by ¬r")