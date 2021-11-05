import os

from SymbolTable import SymbolTable
from re import fullmatch
from tokenize import TokenInfo, generate_tokens


class Scanner:
    # Constants
    RESERVED_KEYWORD = 1
    OPERATOR = 2
    NUMBER = 3
    STRING = 4
    NEWLINE = 5  # end of statement
    IDENTIFIER = 6

    # Init empty scanner
    def __init__(self):
        self.st = SymbolTable(dict)
        self.pif = []

        # Pattern for finding integers
        self.intPattern = r'0|([+-]?0\.[0-9]+)|([+-]?[1-9][0-9]*(\.?[0-9]+)?)'
        # Pattern for finding strings
        self.strPattern = r'"[a-zA-Z_0-9 =]*"'

        # Boolean type
        self.booleans = ("True", "False")

        # Allowed operators
        self.operators = ['+', '-', '/', '//', '%', '*', '**', '=', '+=', '-=', '/=', '//=', '**=', '<', '<=', '==', '=>', '>', 'and', 'or', '!', '~', '&', '|', '^', '<<', '>>', '{', '}', '[', ']', '(', ')', ':', ',', '.', '->', '"']
        # Reserved keywords
        self.reservedKeywords = ['int', 'str', 'bool', 'True', 'False', 'def', 'return', 'if', 'else', 'while', 'for', 'in']

        # Token types we can find in file.brr
        self.tokenTypes = {
            1: self.checkName,
            54: self.checkOp,
            2: self.checkNumber,
            3: self.checkString,
            4: self.checkNewline
        }

        # Original file path
        self.file = ""
        # Temporary file that will contain a clean copy of aforementioned file with no comments
        self.fileTemp = ""

        self.definingFunction = False

    # Creating said temporary file (at the start of scanning)
    def createCleanTemp(self):
        with open(self.file, 'r') as original:
            with open(self.fileTemp, 'w') as temp:
                while line := original.readline():
                    temp.write(remove_comments(line))

    # Deleting said temporary file (at the end of scanning)
    def deleteTemp(self):
        if os.path.exists(self.fileTemp):
            os.remove(self.fileTemp)

    # Called if an error occurs during scanning
    def raiseError(self, token: TokenInfo):
        print(f"""Lexical error at line: {token.start[0]}  <{token.start[1]},{token.end[1]}>
    Error processing token: {token.string}
        Inside file: {self.file}""")

    # Scan the file
    def parseFile(self, filename):
        # Init files
        self.file = filename
        self.fileTemp = f'brrTempFile.{self.file}'

        # Create clean temporary file
        self.createCleanTemp()

        # Read original file and copy contents in temp
        with open(self.fileTemp, 'r') as f:
            tokens = generate_tokens(f.readline)
            for token in tokens:
                self.tokenTypes.get(token.type, self.noOp)(token)

        # Write pif in a file
        with open(f'{self.file}.pif', 'w') as f:
            print(*self.pif, sep='\n', file=f)

        # Write st in a file
        with open(f'{self.file}.st', 'w') as f:
            print(*self.st.getAll(), sep='\n', file=f)

        # Delete temporary file because it is not needed anymore
        self.deleteTemp()

    # Checks whether token is a reserved keyword or an identifier
    def checkName(self, token: TokenInfo):
        if token.string in self.reservedKeywords:
            self.pif.append((self.RESERVED_KEYWORD, token.string))
            return

        self.pif.append((self.IDENTIFIER, self.st + token.string))

    # Checks whether token is an operator
    def checkOp(self, token: TokenInfo):
        if token.string not in self.operators:
            self.raiseError(token)
            return

        self.pif.append((self.OPERATOR, token.string))

    # Checks whether token is an integer
    def checkNumber(self, token: TokenInfo):
        if fullmatch(self.intPattern, token.string):
            self.pif.append((self.NUMBER, token.string))
            return

        self.raiseError(token)

    # Checks whether token is an string
    def checkString(self, token: TokenInfo):
        if fullmatch(self.strPattern, token.string):
            self.pif.append((self.STRING, token.string))
            return

        self.raiseError(token)

    # Checks whether token is the end of a statement (statements must end on \n, for now there isn't anything to check)
    def checkNewline(self, token: TokenInfo):
        ...

    # No-op for anything else found in the file (whitespaces)
    def noOp(self, token: TokenInfo):
        ...


# Helper function for removing comments inside a file.brr
def remove_comments(line, sep="#"):
    return line.split(sep, 1)[0]


def main():
    sc = Scanner()
    sc.parseFile("problem1.brr")
    sc = Scanner()
    sc.parseFile("problem1err.brr")
    sc = Scanner()
    sc.parseFile("problem2.brr")
    sc = Scanner()
    sc.parseFile("problem3.brr")


if __name__ == '__main__':
    main()
