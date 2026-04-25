# Partial meet contraction
# B ÷ φ


from itertools import combinations
from belief_base import BeliefBase
from resolution import is_entailed

def get_remainders(belief_base, formula):
    """Find all maximal subsets of belief_base that do NOT entail formula."""
    beliefs = belief_base.get_sorted()  # list of (formula, priority)
    formulas = [f for f, p in beliefs]
    remainders = []

    # Try all subsets from largest to smallest
    for size in range(len(formulas), -1, -1):
        for subset in combinations(range(len(formulas)), size):
            subset_formulas = [formulas[i] for i in subset]
            if not is_entailed(subset_formulas, formula):
                # Check it's maximal: no formula outside it can be added
                is_maximal = True
                outside = [f for i, f in enumerate(formulas) if i not in subset]
                for extra in outside:
                    if not is_entailed(subset_formulas + [extra], formula):
                        is_maximal = False
                        break
                if is_maximal:
                    remainders.append(subset_formulas)
        if remainders:
            break  # found maximal subsets at this size, stop

    return remainders

def selection_function(remainders, belief_base):
    """Pick the best remainders using priority — keep highest-priority beliefs."""
    if not remainders:
        return []
    beliefs = belief_base.get_sorted()
    priority_map = {f: p for f, p in beliefs}

    def score(remainder):
        return sum(priority_map.get(f, 0) for f in remainder)

    best_score = max(score(r) for r in remainders)
    return [r for r in remainders if score(r) == best_score]

def contract(belief_base, formula):
    """Partial meet contraction: remove formula from belief base."""
    # If belief base doesn't entail formula, nothing to do
    if not is_entailed(belief_base.get_formulas(), formula):
        return belief_base

    remainders = get_remainders(belief_base, formula)
    if not remainders:
        new_bb = BeliefBase()
        return new_bb

    selected = selection_function(remainders, belief_base)

    # Intersection: keep only beliefs in ALL selected remainders
    if not selected:
        return BeliefBase()

    intersection = set(selected[0])
    for r in selected[1:]:
        intersection &= set(r)

# Preserve original insertion order for entrenched beliefs
    new_bb = BeliefBase()
    for f in belief_base.get_formulas():
        if f in intersection:
            new_bb.add(f)
    return new_bb