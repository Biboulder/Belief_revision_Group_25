# Expansion
# B + φ

from belief_base import BeliefBase

def expand(belief_base, formula):
    new_bb = BeliefBase()
    new_bb.beliefs = list(belief_base.beliefs)
    new_bb.add(formula)
    return new_bb