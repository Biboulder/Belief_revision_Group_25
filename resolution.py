# Entailment checking via resolution 
# - Convert formulas to CNF (Conjunctive Normal Form) (cnf.py)
# - Apply the resolution rule repeatedly (resolution.py)
# - If you derive False (empty clause), the set is unsatisfiable 

# Negate φ, convert to CNF
# Add to B's clauses
# Repeatedly apply resolution
# If you derive the empty clause → entailment holds ✓