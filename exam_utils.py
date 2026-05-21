from belief_base import BeliefBase
from contraction import get_remainders, contract
from revision import revise
from resolution import is_entailed
from parser import Parser


def _parse(s):
    return Parser(s).parse()


def banner(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def show_remainders(bb, formula):
    remainders = get_remainders(bb, formula)
    print(f"  A ÷ {formula}  —  {len(remainders)} remainder(s):")
    for i, r in enumerate(remainders):
        print(f"  [{i}] {{{', '.join(str(f) for f in r)}}}")
    return remainders


def check_remainder_membership(bb, formula, candidates):
    remainders = get_remainders(bb, formula)
    remainder_sets = [frozenset(str(f) for f in r) for r in remainders]
    for candidate in candidates:
        candidate_set = frozenset(str(f) for f in candidate)
        label = "{" + ", ".join(str(f) for f in candidate) + "}"
        print(f"  {label} ∈ A ÷ {formula} ?  {candidate_set in remainder_sets}")


def check_entailment_list(bb_or_formulas, candidates):
    if isinstance(bb_or_formulas, BeliefBase):
        formulas = bb_or_formulas.get_formulas()
    else:
        formulas = list(bb_or_formulas)
    for s in candidates:
        f = _parse(s)
        print(f"  B |= {f} ?  {is_entailed(formulas, f)}")


def show_plausibility(bb):
    for f, score in bb.get_sorted():
        print(f"  e={score} {f}")


def show_belief_base(bb, label="Belief base"):
    print(f"\n{label}:")
    beliefs = bb.get_sorted()
    if not beliefs:
        print("  (empty)")
    else:
        for f, score in beliefs:
            print(f"  e={score}  {f}")


def run_exam_exercise(label, base_formulas, contract_formula=None, revise_formula=None,
                      check_formulas=None, check_remainder_candidates=None):
    banner(label)

    bb = BeliefBase()
    for s in base_formulas:
        bb.add(_parse(s))

    show_belief_base(bb, "Initial belief base")

    current_bb = bb

    if check_remainder_candidates is not None and contract_formula is not None:
        cf = _parse(contract_formula)
        print(f"\nRemainder set:")
        show_remainders(bb, cf)
        print(f"\nCandidate membership:")
        parsed_candidates = [[_parse(s) for s in cand] for cand in check_remainder_candidates]
        check_remainder_membership(bb, cf, parsed_candidates)

    if contract_formula is not None:
        cf = _parse(contract_formula)
        current_bb = contract(bb, cf)
        show_belief_base(current_bb, f"After contraction by {cf}")

    if revise_formula is not None:
        rf = _parse(revise_formula)
        current_bb = revise(current_bb, rf)
        show_belief_base(current_bb, f"After revision by {rf}")

    if check_formulas is not None:
        print(f"\nEntailment check on result:")
        check_entailment_list(current_bb, check_formulas)
