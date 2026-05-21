# Demo / runner
from formula import Atom, Not, And, Or, Implies
from belief_base import BeliefBase
from contraction import contract
from revision import revise
from resolution import is_entailed
from agm_tests import run_all_tests
from exam_utils import banner, show_belief_base, run_exam_exercise


def demo():
    banner("Basic Belief Revision Demo")
    p = Atom('p')
    q = Atom('q')

    bb = BeliefBase()
    bb.add(p)
    bb.add(Implies(p, q))
    show_belief_base(bb, "Initial: B = {p, p→q}")

    contracted = contract(bb, q)
    show_belief_base(contracted, "After contracting by q")

    revised = revise(bb, Not(p))
    show_belief_base(revised, "After revising by ~p")

    print("\nEntailment on revised base:")
    for f, s in [(p, "p"), (q, "q"), (Not(p), "~p")]:
        print(f"  B |= {s} ?  {is_entailed(revised.get_formulas(), f)}")


def exam_demo():
    run_exam_exercise(
        label="Exercise 1 — Plausibility order / belief set contraction and revision",
        base_formulas=["p", "q", "p -> q", "p <-> q"],
        contract_formula="p",
        revise_formula="~p",
        check_formulas=["p", "q", "~p", "p & q", "p | q", "p -> q"],
    )

    run_exam_exercise(
        label="2026 Practice Exam: A = {p, q, p&q, p|q}, compute A÷p",
        base_formulas=["p", "q", "p & q", "p | q"],
        contract_formula="p",
        check_remainder_candidates=[
            ["q"],
            ["p", "q", "p & q", "p | q"],
            ["p", "q", "p | q"],
            ["q", "p & q"],
            ["p", "q"],
            ["q", "p & q", "p | q"],
            ["p", "q", "p & q"],
            ["q", "p | q"],
            ["p & q", "p | q"],
            ["p", "p & q"],
            ["p", "p | q"],
            ["p", "p & q", "p | q"],
        ],
        revise_formula="~p",
        check_formulas=["p", "q", "~p", "p & q", "p | q", "p -> q"],
    )


if __name__ == "__main__":
    demo()

    banner("AGM Postulate Tests")
    p = Atom('p')
    q = Atom('q')
    r = Atom('r')

    bb1 = BeliefBase()
    bb1.add(p)
    bb1.add(Implies(p, q))
    run_all_tests(bb1, q, label="No conflict: B={p, p→q}, revise by q")

    bb2 = BeliefBase()
    bb2.add(p)
    bb2.add(Implies(p, q))
    run_all_tests(bb2, Not(p), label="Conflict: B={p, p→q}, revise by ¬p")

    bb3 = BeliefBase()
    bb3.add(p)
    run_all_tests(bb3, And(p, Not(p)), label="Contradiction: B={p}, revise by p∧¬p")

    bb4 = BeliefBase()
    bb4.add(r)
    run_all_tests(bb4, And(p, q), formula2=And(q, p), label="Extensionality: φ=p∧q, ψ=q∧p")

    bb5 = BeliefBase()
    bb5.add(p)
    bb5.add(q)
    bb5.add(Implies(p, r))
    bb5.add(Implies(q, r))
    run_all_tests(bb5, Not(r), label="Rich base: B={p,q,p→r,q→r}, revise by ¬r")

    banner("Exam exercises")
    exam_demo()
