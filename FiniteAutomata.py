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

    # Reads the given fa from a file, the fa must be in a json format
    def readFa(self):
        if self.fileName is None:
            return

        # Parses the json formatted fa and sets the attributes of the fa
        with open(self.fileName) as f:
            finiteAutomata = json.load(f, object_hook=finiteAutomataDecoder)
            self.__init__(*finiteAutomata)

    # Parses the sequence given as a string
    def parseSequence(self, sequence: str):
        # Initializes the current state
        current = self.initialState
        print(current)
        # Loops over the sequence
        for element in sequence:
            # Tries to make a transition
            current = self.makeTransition(current, element)
            # There is no valid transition
            if current is None:
                print('Sequence is not valid for this automata.')
                return

            print(current)

        # After the sequence is over, check is we are in a final state
        if current in self.finalStates:
            print('Sequence successfully parsed.')
            return

        print('Sequence does not end on a final state.')

    # Tries to make a transition, if it succeeds then the next state is returned otherwise None
    def makeTransition(self, start, element):
        # Loops over the available transitions
        for transition in self.transitions:
            # If there is a transition starting with that state with that load the following state is returned otherwise None
            if transition.start == start and transition.load == element:
                return transition.end

        return None

    # Gets user input for the sequence and starts parsing it
    def startSequence(self, _):
        sequence = input("Sequence: ")
        self.parseSequence(sequence)

    # Shows the menu
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


# Helper function for converting json to class
def finiteAutomataDecoder(finiteAutomataDict):
    return namedtuple('FiniteAutomata', finiteAutomataDict.keys())(*finiteAutomataDict.values())


def main():
    fa = FiniteAutomata(fileName="fa.in")


if __name__ == '__main__':
    main()
