import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Demo / runner — walks through the stages from the assignment brief:
#   1. belief base
#   2. logical entailment (resolution)
#   3. contraction (partial meet)
#   4. expansion
#   5. revision (Levi identity)
# and finishes by running the AGM postulate test suite.

from formula import Atom, Not, And, Implies
from belief_base import BeliefBase
from parser import Parser
from resolution import is_entailed, is_consistent
from contraction import contract
from expansion import expand
from revision import revise
import agm_tests


def parse(s):
    return Parser(s).parse()


def banner(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def show(bb, label="Belief base"):
    print(f"\n{label}:")
    if not bb.get_formulas():
        print("  (empty)")
        return
    for f, e in bb.get_sorted():
        print(f"  e={e}  {f}")


def demo():
    banner("Stage 1 — Belief base")
    # B = { p, p -> q, q -> r }   (insertion order = entrenchment)
    bb = BeliefBase()
    bb.add(parse("p"))
    bb.add(parse("p -> q"))
    bb.add(parse("q -> r"))
    show(bb)

    banner("Stage 2 — Logical entailment (resolution)")
    for s in ["q", "r", "~p", "p & r"]:
        phi = parse(s)
        print(f"  B |= {phi}  ?  {is_entailed(bb.get_formulas(), phi)}")
    print(f"  B is consistent?  {is_consistent(bb.get_formulas())}")

    banner("Stage 3 — Contraction:  B ÷ r")
    # remove r: must drop something from {p, p->q, q->r} so r is no longer derivable
    contracted = contract(bb, parse("r"))
    show(contracted, "B ÷ r")
    print(f"\n  (B ÷ r) |= r  ?  {is_entailed(contracted.get_formulas(), parse('r'))}")

    banner("Stage 4 — Expansion:  B + s")
    expanded = expand(bb, parse("s"))
    show(expanded, "B + s")

    banner("Stage 5 — Revision (Levi identity):  B * ~r  =  (B ÷ r) + ~r")
    revised = revise(bb, parse("~r"))
    show(revised, "B * ~r")
    print(f"\n  (B * ~r) |= ~r  ?  {is_entailed(revised.get_formulas(), parse('~r'))}")
    print(f"  B * ~r is consistent?  {is_consistent(revised.get_formulas())}")


if __name__ == "__main__":
    print("Belief Revision Engine — Group 25")
    demo()

    banner("AGM postulate test suite")
    # Delegate to the existing scenarios in agm_tests.py
    p, q, r = Atom('p'), Atom('q'), Atom('r')

    bb1 = BeliefBase(); bb1.add(p); bb1.add(Implies(p, q))
    agm_tests.run_all_tests(bb1, q, label="No conflict: B={p, p->q}, revise by q")

    bb2 = BeliefBase(); bb2.add(p); bb2.add(Implies(p, q))
    agm_tests.run_all_tests(bb2, Not(p), label="Conflict: B={p, p->q}, revise by ¬p")

    bb3 = BeliefBase(); bb3.add(p)
    agm_tests.run_all_tests(bb3, And(p, Not(p)), label="Contradiction: B={p}, revise by p∧¬p")

    bb4 = BeliefBase(); bb4.add(r)
    agm_tests.run_all_tests(bb4, And(p, q), formula2=And(q, p),
                            label="Extensionality: φ=p∧q, ψ=q∧p")

    bb5 = BeliefBase()
    for f in (p, q, Implies(p, r), Implies(q, r)):
        bb5.add(f)
    agm_tests.run_all_tests(bb5, Not(r), label="Rich base: B={p,q,p->r,q->r}, revise by ¬r")
