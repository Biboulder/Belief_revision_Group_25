# Expansion
# B + φ


from belief_base import BeliefBase

def expand(belief_base, formula, priority=1):
    """Return a new BeliefBase with formula added at the given priority."""
    new_bb = BeliefBase()
    new_bb.beliefs = list(belief_base.beliefs)
    new_bb.add(formula, priority)
    return new_bb