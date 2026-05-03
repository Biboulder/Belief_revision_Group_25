#
#   <->   biconditional    — left-associative
#   ->    implication      — right-associative
#   |     disjunction      — left-associative
#   &     conjunction      — left-associative
#   ~     negation, unary  — right-associative (handles ~~p naturally)
#
#   The chain:
#   parse -> parse_biconditional -> parse_implication -> parse_or
#         -> parse_and -> parse_not -> parse_atom
#

from formula import Atom, Not, And, Or, Implies, Biconditional

class Parser:
    def __init__(self, text):
        # Tokenize: split into list of tokens
        # e.g. "p -> q" → ['p', '->', 'q']
        self.tokens = self.tokenize(text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        return self.parse_biconditional()

    def parse_biconditional(self):
        left = self.parse_implication()
        while self.peek() == '<->':
            self.consume()
            right = self.parse_implication()
            left = Biconditional(left, right)
        return left

    def parse_implication(self):
        left = self.parse_or()
        if self.peek() == '->':
            self.consume()
            right = self.parse_implication()  # right-associative
            return Implies(left, right)
        return left

    def parse_or(self):
        left = self.parse_and()
        while self.peek() == '|':
            self.consume()
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek() == '&':
            self.consume()
            right = self.parse_not()
            left = And(left, right)
        return left

    def parse_not(self):
        if self.peek() == '~':
            self.consume()
            return Not(self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.consume()
        if tok == '(':
            expr = self.parse_biconditional()
            self.consume()
            return expr
        return Atom(tok)
    
    def tokenize(self, text):
        text = text.replace('<->', ' BICONDITIONAL ')
        text = text.replace('->', ' -> ')
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        text = text.replace('~', ' ~ ')
        text = text.replace('&', ' & ')
        text = text.replace('|', ' | ')
        text = text.replace('BICONDITIONAL', '<->')
        return text.split()