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
        self.constructTable()

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
        self.follow[tuple([self.grammar.start])].add('E')
        isSetChanged = False
        for key, value in self.grammar.productions.items():
            for v in value.right:
                for i in range(len(v)):
                    if self.grammar.isTerminal(v[i]):
                        continue
                    copySet = self.follow[tuple([v[i]])]
                    if i < len(v) - 1:
                        copySet = copySet.union(self.innerLoop(copySet, v[i + 1:], self.follow[key]))
                    else:
                        copySet = copySet.union(self.follow[key])

                    if len(self.follow[tuple([v[i]])]) != len(copySet):
                        self.follow[tuple([v[i]])] = copySet
                        isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for key, value in self.grammar.productions.items():
                for v in value.right:
                    for i in range(len(v)):
                        if self.grammar.isTerminal(v[i]):
                            continue
                        copySet = self.follow[tuple([v[i]])]
                        if i < len(v) - 1:
                            copySet = copySet.union(self.innerLoop(copySet, v[i + 1:], self.follow[key]))
                        else:
                            copySet = copySet.union(self.follow[key])

                        if len(self.follow[tuple([v[i]])]) != len(copySet):
                            self.follow[tuple([v[i]])] = copySet
                            isSetChanged = True

    def constructTable(self):
        nonTerminals = self.grammar.nonTerminals
        terminals = self.grammar.terminals

        for key, value in self.grammar.productions.items():
            rowSymbol = key
            for v in value.right:
                rule = v[0].replace("'", "")
                for columnSymbol in terminals | ['E']:
                    pair = (rowSymbol[0], columnSymbol)
                    # rule 1 part 1
                    if rule == columnSymbol and columnSymbol != 'E':
                        self.table[pair] = v
                    elif rule in nonTerminals and "'"+columnSymbol+"'" in self.first[tuple(rule)]:
                        if pair not in self.table.keys():
                            self.table[pair] = v
                        else:
                            print(pair)
                            print("Grammar is not LL(1).")
                            assert False
                    else:
                        if rule == 'E':
                            for b in self.follow[rowSymbol]:
                                if b == 'E':
                                    b = '$'
                                self.table[(rowSymbol[0], b)] = v
                        else:
                            # rule 1 part 2
                            firsts = set()
                            for production in self.grammar.productions[rowSymbol].right:
                                for symbol in production:
                                    if symbol in nonTerminals:
                                        firsts = firsts | self.first[tuple([symbol])]
                                if 'E' in firsts:
                                    for b in self.follow[rowSymbol]:
                                        if b == 'E':
                                            b = '$'
                                        if (rowSymbol[0], b) not in self.table.keys():
                                            self.table[(rowSymbol[0], b)] = v

        # rule 2
        for t in terminals:
            self.table[(t, t)] = ('pop', -1)

        # rule 3
        self.table[('$', '$')] = ('acc', -1)


if __name__ == '__main__':
    g = Grammar(fileName="g1.txt")
    p = Parser(g)
    print(p.first)
    print(p.follow)
    print(p.table)
