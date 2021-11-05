

class Transition:
    def __init__(self, transition: str):
        self.start, self.load, self.end = transition.replace(' ', '').split('->')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.start} -> {self.end}'
