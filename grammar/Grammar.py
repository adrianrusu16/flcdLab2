import json
from collections import namedtuple, OrderedDict
from typing import Optional


class Grammar:

    def __init__(self, non_terminals=None, terminals=None, starting_symbol=None, productions=None):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.starting_symbol = starting_symbol
        self.productions = OrderedDict() if productions is None else self.parse_productions(productions)

    def from_file(self, file):

        if file is None:
            return
        # Parses the json formatted fa and sets the attributes of the fa
        with open(file) as f:
            grammar = json.load(f, object_hook=grammarDecoder)
            self.__init__(*grammar)

    @staticmethod
    def parse_productions(productions) -> Optional[OrderedDict]:
        if productions is None:
            return None

        productionsDict = OrderedDict()

        for transition in productions:
            key, value = transition.split("::=")
            productionsDict[key.strip()] = value.strip().split(" | ")

        return productionsDict

    def get_productions_for(self, non_terminal):
        if non_terminal not in self.non_terminals:
            return []
        if non_terminal in self.productions.keys():
            return self.productions[non_terminal]

    def get_productions_of(self, character):
        to_return = []
        for key in self.productions.keys():
            for production in self.productions[key]:
                if character in production.split(" "):
                    to_return.append((key, production))
        return to_return

    def is_cfg(self):
        for production in self.productions:
            if len(self.productions[production]) != 1:
                return False
        return True

    def get_terminals(self):
        return self.terminals

    def __str__(self):
        return "nonTerminals: " + str(self.non_terminals) + "\n" + \
               "terminals: " + str(self.terminals) + "\n" + \
               "productions: " + str(self.productions) + "\n" + \
               "startingSymbol: " + str(self.starting_symbol) + "\n"


# Helper function for converting json to class
def grammarDecoder(grammarDict):
    return namedtuple('FiniteAutomata', grammarDict.keys())(*grammarDict.values())


if __name__ == "__main__":
    g = Grammar()
    g.from_file("g1.txt")
    print(g)
    print(g.get_productions_of('B'))
