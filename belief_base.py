# Belief base with priorities
# EX B = { p, p → q, ¬r }


class BeliefBase:
    def __init__(self):
        # Ordered list of formulas — index 0 = most entrenched (added first)
        self.beliefs = []

    def add(self, formula):
        if formula not in self.beliefs:
            self.beliefs.append(formula)  # newest = least entrenched

    def remove(self, formula):
        self.beliefs = [f for f in self.beliefs if f != formula]

    def get_formulas(self):
        return list(self.beliefs)

    def get_sorted(self):
        # Returns (formula, entrenchment) where lower index = more entrenched
        return [(f, len(self.beliefs) - i) for i, f in enumerate(self.beliefs)]

    def __str__(self):
        if not self.beliefs:
            return "BeliefBase: (empty)"
        lines = ["BeliefBase (most entrenched first):"]
        for i, f in enumerate(self.beliefs):
            lines.append(f"  {i+1}. {f}")
        return "\n".join(lines)