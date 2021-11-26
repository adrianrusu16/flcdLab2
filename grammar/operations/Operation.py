from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self, load):
        self.load = load

    @abstractmethod
    def __call__(self):
        pass
