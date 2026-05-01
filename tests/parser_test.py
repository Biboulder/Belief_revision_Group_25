import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from parser import Parser


test_cases = [
    "p",
    "~p",
    "p & q",
    "p | q",
    "p -> q",
    "p <-> q",
    "~(p & q)",
    "p -> (q & ~r)",
    "(p | q) & (r | s)",
    "~~p",
]

for tc in test_cases:
    parsed = Parser(tc).parse()
    print(f"Input:  {tc}")
    print(f"Parsed: {parsed}")
    print()