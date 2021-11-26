from ordered_set import OrderedSet

from grammar.Grammar import Grammar


class Parser:
    def __init__(self, grammar: Grammar):
        self. grammar = grammar
        self.first = {nonTerminal: OrderedSet() for nonTerminal in self.grammar.nonTerminals}
        self.follow = {nonTerminal: OrderedSet() for nonTerminal in self.grammar.nonTerminals}
        self.table = {}
        self.constructFirst()
        self.constructFollow()

    def constructFirst(self):
        setChanged = False

        for left, right in self.grammar.productions:
            for sequence in right:
                nonTerminal = left.load
                tempSet = self.first[nonTerminal] | self.grammar.getTerminalsFromProduction(nonTerminal)

                if len(self.first[nonTerminal]) != len(tempSet):
                    self.first[nonTerminal] = tempSet
                    setChanged = True

        while setChanged:
            setChanged = False
            for left, right in self.grammar.productions:
                for sequence in right:
                    nonTerminal = left.load
                    tempSet = self.first[nonTerminal] | self.grammar.getTerminalsFromProduction(nonTerminal)

                    if len(self.first[nonTerminal]) != len(tempSet):
                        self.first[nonTerminal] = tempSet
                        setChanged = True

    def constructFollow(self):
        pass

