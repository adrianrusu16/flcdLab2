import json
from collections import namedtuple, OrderedDict
from typing import Optional
from ordered_set import OrderedSet

from GrammarParsingException import GrammarParsingException
from grammar.operations.SequenceOperation import SequenceOperation
from operations.NonTerminal import NonTerminal
from operations.Terminal import Terminal
from operations.ChooseOneOperation import *
from operations.OptionalOperation import *
from operations.RepeatOperation import *
from Production import Production


class Grammar:

    def __init__(self, states=None, alphabet=None, initialState=None, transitions=None, fileName=None):
        self.nonTerminals = OrderedSet(states) if states is not None else None
        self.terminals = OrderedSet(alphabet) if alphabet is not None else None
        self.start = initialState
        self.productions = self.parseTransitions(transitions)

        self.specialOpsSE = {'(': ')', '[': ']', '{': '}'}
        self.specialOpsES = {v: k for k, v in self.specialOpsSE.items()}

        self.opMap = {
            "'": Terminal,
            '(': ChooseOneOperation,
            '[': OptionalOperation,
            '{': RepeatOperation
        }

        if fileName is not None:
            self.fileName = fileName
            self.readGrammar()
            print(self.isCFG())

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
                left=self.checkLeft(left.strip() + ' '),
                right=self.checkRight(right.strip())
            )

            productionsDict[production.left.load] = production

        return productionsDict

    def checkLeft(self, left: str) -> SequenceOperation:
        return self.getOps(left)

    def checkRight(self, right: str) -> OrderedSet[SequenceOperation]:
        rights = right.split("|")

        ops = OrderedSet()

        for right in rights:
            ops.add(self.getOps(right.strip() + ' '))

        return ops

    def getOps(self, string: str) -> SequenceOperation:
        ops = []
        specials = []
        lastSpace = -1
        isString = False
        finishedSpecial = False
        for index, character in enumerate(string):
            if character == "'":
                if not isString:
                    specials.append((character, index))
                else:
                    special = specials.pop(-1)
                    ops.append(self.opMap.get(special[0])(string[special[1]:index+1]))
                    finishedSpecial = True

                isString = not isString
            elif not isString:
                if self.specialOpsSE.get(character, None) is not None:  # starting symbol
                    specials.append((character, index))

                elif self.specialOpsES.get(character, None) is not None:  # ending symbol
                    if len(specials) == 0:
                        raise GrammarParsingException("Closing symbol does not have an opening one")

                    if self.specialOpsSE.get(specials[-1][0]) != character:
                        raise GrammarParsingException("Closing symbol does not correspond to its opening symbol")

                    special = specials.pop(-1)
                    ops.append(self.opMap.get(special[0])(self.getOps(string[special[1]+1:index])))
                    finishedSpecial = True

                elif character == " ":
                    if not finishedSpecial:
                        if len(specials) == 0:
                            op = string[lastSpace+1:index]
                            if op in self.nonTerminals:
                                ops.append(NonTerminal(op))

                            elif op in self.terminals:
                                ops.append(Terminal(op))

                            else:
                                raise GrammarParsingException("Operand is neither defined as a terminal nor non-terminal")

                    lastSpace = index
                    finishedSpecial = False

        return SequenceOperation(tuple(ops))

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

    def getTerminalsFromProduction(self, nonTerminal):
        production = self.productions.get(tuple([NonTerminal(nonTerminal)]), None)
        if production is None:
            return None

        terminals = OrderedSet()
        for sequence in production.right:
            for operation in sequence.load:
                if isinstance(operation, Terminal):
                    terminals.add(operation)

        return terminals


# Helper function for converting json to class
def grammarDecoder(grammarDict):
    return namedtuple('FiniteAutomata', grammarDict.keys())(*grammarDict.values())


def main():
    g = Grammar(fileName="g2.txt")


if __name__ == '__main__':
    main()
