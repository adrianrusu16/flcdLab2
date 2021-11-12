

class Transition:
    def __init__(self, transition: str):
        self.start, self.load, self.end = transition.replace(' ', '').split('->')
        self.load = int(self.load)

    def __key(self):
        return self.start, self.load, self.end

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.start} -> {self.load} -> {self.end}'
