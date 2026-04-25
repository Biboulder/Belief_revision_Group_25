# Levi identity (contract + expand)
# B * φ = (B ÷ ¬φ) + φ


from formula import Not
from contraction import contract
from expansion import expand

def revise(belief_base, formula):
    contracted = contract(belief_base, Not(formula))
    return expand(contracted, formula)