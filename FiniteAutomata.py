import json
from collections import namedtuple

from Transition import Transition


class FiniteAutomata:

    def __init__(self, states=None, alphabet=None, initialState=None, finalStates=None, transitions=None, fileName=None):
        self.states = states
        self.alphabet = alphabet
        self.initialState = initialState
        self.finalStates = finalStates
        self.transitions = [Transition(transition) for transition in transitions] if transitions is not None else None
        self.fileName = fileName

        self.menuLoop = False

        self.menuOptions = {
            '1': self.printElement,
            '2': self.printElement,
            '3': self.printElement,
            '4': self.printElement,
            '5': self.startSequence,
            '0': self.stopMenuLoop
        }

        self.menuOptionsDescriptions = {
            '1': "Show the set of states.",
            '2': "Show the alphabet.",
            '3': "Show the transitions.",
            '4': "Show the set of final states.",
            '5': "Parse sequence",
            '0': "Exit."
        }

        self.prints = {
            '1': 'states',
            '2': 'alphabet',
            '3': 'transitions',
            '4': 'finalStates'
        }

        if fileName is not None:
            self.readFa()
            self.showMenu()

    def readFa(self):
        if self.fileName is None:
            return

        with open(self.fileName) as f:
            finiteAutomata = json.load(f, object_hook=finiteAutomataDecoder)
            self.__init__(*finiteAutomata)

    def parseSequence(self, sequence: str):
        current = self.initialState
        print(current)
        for element in sequence:
            current = self.makeTransition(current, element)
            if current is None:
                print('Sequence is not valid for this automata.')
                return

            print(current)

        if current in self.finalStates:
            print('Sequence successfully parsed.')
            return

        print('Sequence does not end on a final state.')

    def makeTransition(self, start, element):
        for transition in self.transitions:
            if transition.start == start and transition.load == element:
                return transition.end

        return None

    def startSequence(self, _):
        sequence = input("Sequence: ")
        self.parseSequence(sequence)

    def showMenu(self):
        self.menuLoop = True
        while self.menuLoop:
            for option, description in self.menuOptionsDescriptions.items():
                print(f'{option}. {description}')

            option = input('>>>')
            self.menuOptions.get(option, self.menuOptionError)(option)

    def printElement(self, option):
        print(self.__getattribute__(self.prints[option]))

    def stopMenuLoop(self, _):
        self.menuLoop = False

    def menuOptionError(self, option):
        print(f'Option <{option}> does not exist.')


def finiteAutomataDecoder(finiteAutomataDict):
    return namedtuple('FiniteAutomata', finiteAutomataDict.keys())(*finiteAutomataDict.values())


def main():
    fa = FiniteAutomata(fileName="fa.in")


if __name__ == '__main__':
    main()
