from abc import ABC
from collections.abc import MutableMapping


class HashMap(MutableMapping, ABC):
    def __init__(self, length=100):
        self.map = [None for _ in range(length)]
        self.length = 0

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def keys(self):
        pass

    def pop(self, key, returnValue=None):
        pass

