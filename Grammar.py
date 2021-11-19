import json
from collections import namedtuple


class Grammar:

    def __init__(self, N=None, Sigma=None, S=None, P=None, fileName=None):
        self.nonTerminals = N
        self.terminals = Sigma
        self.startingSymbol = S
        self.productions = {}
        self.fileName = fileName
        if self.fileName is not None:
            self.fromFile()

        self.productionsTemp = P if P is not None else {}

    def fromFile(self):
        if self.fileName is None:
            return

        # Parses the json formatted fa and sets the attributes of the fa
        with open(self.fileName) as f:
            finiteAutomata = json.load(f, object_hook=grammarDecoder)
            self.__init__(*finiteAutomata)

            for production in self.productionsTemp:
                key = production.split('->')[0]
                value = production.strip().split('->')[1]
                if key not in self.productions:
                    self.productions[key] = [value]
                else:
                    self.productions[key].append(value)

    def getProductionsFor(self, nonTerminal):
        if nonTerminal not in self.nonTerminals:
            raise Exception('Can only show productions for non-terminals')
        if nonTerminal in self.productions:
            return self.productions[nonTerminal]

    def isCFG(self):
        for prod in self.productions:
            if len(self.productions[prod]) != 1:
                return False

        return True

    def __str__(self):
        return f"terminals (N) : {self.terminals}\n" \
               f"nonterminals (Sigma) : {self.nonTerminals}\n" \
               f"productions (P) : {self.productions}\n" \
               f"startingSymbol (S) : {self.startingSymbol}\n"


# Helper function for converting json to class
def grammarDecoder(grammarDict):
    return namedtuple('Grammar', grammarDict.keys())(*grammarDict.values())


g = Grammar(fileName="g1.txt")
print(g)
print(g.isCFG())
print(g.getProductionsFor('A'))
