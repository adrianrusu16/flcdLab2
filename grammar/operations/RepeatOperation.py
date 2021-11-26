from grammar.operations.Operation import Operation


class RepeatOperation(Operation):

    def __call__(self):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{{{str(self.load)}}}'

    def __key(self):
        return str(self.load)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, RepeatOperation):
            return self.__key() == other.__key()
        return NotImplemented
