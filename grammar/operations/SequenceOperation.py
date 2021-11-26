from grammar.operations.Operation import Operation


class SequenceOperation(Operation):

    def __init__(self, load: list[Operation]):
        super().__init__(load)

    def __call__(self):
        pass

    def __len__(self):
        return len(self.load)

    def __contains__(self, item):
        return item in self.load

    def __key(self):
        return str(self.load)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, SequenceOperation):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return str(self)

    def __str__(self):
        prod = ''
        for op in self.load:
            prod += str(op) + ' '
        else:
            prod = prod[:-1]

        return prod
