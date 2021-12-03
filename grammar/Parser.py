from ordered_set import OrderedSet

from grammar.Grammar import Grammar


class Parser:
    def __init__(self, grammar: Grammar):
        self. grammar = grammar
        self.first = {tuple([nonTerminal]): OrderedSet() for nonTerminal in self.grammar.nonTerminals}
        self.follow = {tuple([nonTerminal]): OrderedSet() for nonTerminal in self.grammar.nonTerminals}
        self.table = {}
        self.constructFirst()
        self.constructFollow()

    def innerLoop(self, initialSet, items, additionalSet):
        copySet = initialSet
        for i in range(len(items)):
            if not self.grammar.isTerminal(items[i]):
                copySet = copySet.union(entry for entry in self.first[tuple([items[i]])] if entry != 'E')
                if 'E' in self.first[tuple([items[i]])]:
                    if i < len(items) - 1:
                        continue
                    copySet = copySet.union(additionalSet)
                    break
                else:
                    break
            else:
                copySet = copySet.union({items[i]})
                break

        return copySet

    def constructFirst(self):
        isSetChanged = False
        for key, value in self.grammar.productions.items():
            for v in value.right:
                copySet = self.first[key]
                copySet = copySet.union(self.innerLoop(copySet, v, ['E']))

                if len(self.first[key]) != len(copySet):
                    self.first[key] = copySet
                    isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for key, value in self.grammar.productions.items():
                for v in value.right:
                    copySet = self.first[key]
                    copySet = copySet.union(self.innerLoop(copySet, v, ['E']))

                    if len(self.first[key]) != len(copySet):
                        self.first[key] = copySet
                        isSetChanged = True

    def constructFollow(self):
        pass


if __name__ == '__main__':
    g = Grammar(fileName="g2.txt")
    p = Parser(g)
    print(p.first)

