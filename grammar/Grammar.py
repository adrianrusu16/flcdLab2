import json
from collections import namedtuple, OrderedDict
from typing import Optional
from ordered_set import OrderedSet

from GrammarParsingException import GrammarParsingException
from Production import Production


class Grammar:

    def __init__(self, states=None, alphabet=None, initialState=None, transitions=None, fileName=None):
        self.nonTerminals = OrderedSet(states) if states is not None else None
        self.terminals = OrderedSet(alphabet) if alphabet is not None else None
        self.start = initialState
        self.productions = self.parseTransitions(transitions)
        self.types = []

        if fileName is not None:
            self.fileName = fileName
            self.readGrammar()

    # Reads the given fa from a file, the fa must be in a json format
    def readGrammar(self):
        if self.fileName is None:
            return

        # Parses the json formatted fa and sets the attributes of the fa
        with open(self.fileName) as f:
            grammar = json.load(f, object_hook=grammarDecoder)
            self.__init__(*grammar)

    def parseTransitions(self, transitions) -> Optional[OrderedDict]:
        if transitions is None:
            return None

        productionsDict = OrderedDict()

        for transition in transitions:
            left, right = transition.split("::=")

            production = Production(
                left=self.checkLeft(left.strip()),
                right=self.checkRight(right.strip())
            )

            productionsDict[production.left] = production

        return productionsDict

    def checkLeft(self, left: str):
        return tuple(left.strip().split(' '))

    def checkRight(self, right: str) -> OrderedSet:
        rights = right.split("|")

        ops = OrderedSet()

        for right in rights:
            ops.add(tuple(right.strip().split(' ')))

        return ops

    def isTerminal(self, string: str):
        if string in self.nonTerminals:
            return False
        elif string[0] == string[-1] == "'" and string[1:-1] in self.terminals:
            return True
        else:
            raise GrammarParsingException(f"{string} is neither a terminal nor non-terminal")

    def isCFG(self) -> bool:
        for production in self.productions:
            if len(production) != 1:
                return False

        return True

    def printNonTerminals(self):
        print(*self.nonTerminals, sep='\n')

    def printTerminals(self):
        print(*self.terminals, sep='\n')

    def printProductions(self, nonTerminal=None):
        print(*self.productions.values(), sep='\n') if nonTerminal is None else self.printNonTerminalProduction(nonTerminal)

    def printNonTerminalProduction(self, nonTerminal):
        for production in self.productions:
            if production.isOnlyNonTerminal(nonTerminal):
                print(production)


# Helper function for converting json to class
def grammarDecoder(grammarDict):
    return namedtuple('FiniteAutomata', grammarDict.keys())(*grammarDict.values())


def main():
    g = Grammar(fileName="g2.txt")


if __name__ == '__main__':
    main()
