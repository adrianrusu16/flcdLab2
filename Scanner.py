import os

from SymbolTable import SymbolTable
from re import fullmatch
from tokenize import TokenInfo, generate_tokens


class Scanner:
    RESERVED_KEYWORD = 1
    INDENT = 2
    DEDENT = 3
    OPERATOR = 4
    NUMBER = 5
    STRING = 6
    NEWLINE = 7  # end of statement
    IDENTIFIER = 8  # end of statement

    def __init__(self):
        self.st = SymbolTable(dict)
        self.pif = []

        self.intPattern = r'0|([+-]?0\.[0-9]+)|([+-]?[1-9][0-9]*(\.?[0-9]+)?)'
        self.strPattern = r'"[a-zA-Z_0-9 =]*"'

        self.booleans = ("True", "False")

        self.operators = ['+', '-', '/', '//', '%', '*', '**', '=', '+=', '-=', '/=', '//=', '**=', '<', '<=', '==', '=>', '>', 'and', 'or', '!', '~', '&', '|', '^', '<<', '>>', '{', '}', '[', ']', '(', ')', ':', ',', '.', '->', '"']
        self.reservedKeywords = ['int', 'str', 'bool', 'True', 'False', 'def', 'return', 'if', 'else', 'while', 'for', 'in']

        self.tokenTypes = {
            1: self.checkName,
            54: self.checkOp,
            5: self.checkIndent,
            6: self.checkDedent,
            2: self.checkNumber,
            3: self.checkString,
            4: self.checkNewline
        }

        self.file = ""
        self.fileTemp = ""

        self.definingFunction = False

    def createCleanTemp(self):
        with open(self.file, 'r') as original:
            with open(self.fileTemp, 'w') as temp:
                while line := original.readline():
                    temp.write(remove_comments(line))

    def deleteTemp(self):
        if os.path.exists(self.fileTemp):
            os.remove(self.fileTemp)

    def raiseError(self, token: TokenInfo):
        print(f"""Lexical error at line: {token.start[0]}  <{token.start[1]},{token.end[1]}>
    Error processing token: {token.string}
        Inside file: {self.file}""")

    def parseFile(self, filename):
        self.file = filename
        self.fileTemp = f'brrTempFile.{self.file}'

        self.createCleanTemp()

        with open(self.fileTemp, 'r') as f:
            tokens = generate_tokens(f.readline)
            for token in tokens:
                self.tokenTypes.get(token.type, self.noOp)(token)

        with open(f'{self.file}.pif', 'w') as f:
            print(*self.pif, sep='\n', file=f)

        with open(f'{self.file}.st', 'w') as f:
            print(*self.st.getAll(), sep='\n', file=f)

        self.deleteTemp()

    def checkName(self, token: TokenInfo):
        if token.string in self.reservedKeywords:
            self.pif.append((self.RESERVED_KEYWORD, token.string))
            return

        self.pif.append((self.IDENTIFIER, self.st + token.string))

    def checkOp(self, token: TokenInfo):
        if token.string not in self.operators:
            self.raiseError(token)
            return

        self.pif.append((self.OPERATOR, token.string))

    def checkIndent(self, token: TokenInfo):
        self.pif.append((self.INDENT, token.string))

    def checkDedent(self, token: TokenInfo):
        self.pif.append((self.DEDENT, token.string))

    def checkNumber(self, token: TokenInfo):
        if fullmatch(self.intPattern, token.string):
            self.pif.append((self.NUMBER, token.string))
            return

        self.raiseError(token)

    def checkString(self, token: TokenInfo):
        if fullmatch(self.strPattern, token.string):
            self.pif.append((self.STRING, token.string))
            return

        self.raiseError(token)

    def checkNewline(self, token: TokenInfo):
        ...

    def noOp(self, token: TokenInfo):
        ...


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
