from ordered_set import OrderedSet

from grammar.operations.SequenceOperation import SequenceOperation


class Production:
    def __init__(self, left: SequenceOperation, right: OrderedSet[SequenceOperation]):
        self.left = left
        self.right = right

    def isOnlyNonTerminal(self, nonTerminal) -> bool:
        return self.isCFG() and nonTerminal == self.left.load[0].load

    def isCFG(self) -> bool:
        return len(self.left) == 1

    def __key(self):
        return str(self.left), str(self.right)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Production):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return str(self)

    def __str__(self):
        right = ''
        for op in iter(self.right):
            right += str(op) + ' | '
        else:
            right = right[:-3]

        return f'{str(self.left)} ::= {right}'

    # def __iter__(self):
    #     return self.left, self.right
