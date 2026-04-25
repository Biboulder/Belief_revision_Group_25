# Belief base with priorities
# EX B = { p, p → q, ¬r }


class BeliefBase:
    def __init__(self):
        self.beliefs = []  # list of (formula, priority)

    def add(self, formula, priority=1):
        # Remove if already exists, then add with new priority
        self.beliefs = [(f, p) for f, p in self.beliefs if f != formula]
        self.beliefs.append((formula, priority))

    def remove(self, formula):
        self.beliefs = [(f, p) for f, p in self.beliefs if f != formula]

    def get_formulas(self):
        return [f for f, p in self.beliefs]

    def get_sorted(self):
        return sorted(self.beliefs, key=lambda x: x[1], reverse=True)

    def __str__(self):
        sorted_beliefs = self.get_sorted()
        if not sorted_beliefs:
            return "BeliefBase: (empty)"
        lines = ["BeliefBase:"]
        for f, p in sorted_beliefs:
            lines.append(f"  priority={p}: {f}")
        return "\n".join(lines)