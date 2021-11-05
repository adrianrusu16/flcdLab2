import json
from collections import namedtuple


class FiniteAutomata:

    def __init__(self, states=None, alphabet=None, initialState=None, finalStates=None, transitions=None, fileName=None):
        self.states = states
        self.alphabet = alphabet
        self.initialState = initialState
        self.finalStates = finalStates
        self.transitions = transitions
        self.fileName = fileName

        self.menuLoop = False

        self.menuOptions = {
            '1': self.printElement,
            '2': self.printElement,
            '3': self.printElement,
            '4': self.printElement,
            '0': self.stopMenuLoop
        }

        self.menuOptionsDescriptions = {
            '1': "Show the set of states.",
            '2': "Show the alphabet.",
            '3': "Show the transitions.",
            '4': "Show the set of final states.",
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

    def showMenu(self):
        self.menuLoop = True
        while self.menuLoop:
            for option, description in self.menuOptionsDescriptions.items():
                print(f'{option}. {description}')

            option = input('>>>')
            self.menuOptions[option](option)

    def printElement(self, option):
        print(self.__getattribute__(self.prints[option]))

    def stopMenuLoop(self, _):
        self.menuLoop = False


def finiteAutomataDecoder(finiteAutomataDict):
    return namedtuple('FiniteAutomata', finiteAutomataDict.keys())(*finiteAutomataDict.values())


def main():
    FiniteAutomata(fileName="fa.in")


if __name__ == '__main__':
    main()
