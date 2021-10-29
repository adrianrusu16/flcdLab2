from SymbolTable import SymbolTable
import tokenize
from tokenize import TokenInfo
from re import fullmatch


class Scanner:
    RESERVED_KEYWORD = -1
    INDENT = 1
    DEDENT = 2
    FUNCTION_NAME = 3
    OPERATOR = 4
    NUMBER = 5
    STRING = 6
    NEWLINE = 7  # end of statement

    def __init__(self):
        self.st = SymbolTable(dict)
        self.pif = []
        self.tif = []

        self.intPattern = r'0|([+-]?0\.[0-9]+)|([+-]?[1-9][0-9]*(\.?[0-9]+))'
        self.strPattern = r'"[a-zA-Z_0-9]*"'
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

        self.definingFunction = False

    def raiseError(self, token: TokenInfo):
        ...

    def parseFile(self, filename):
        with open(filename, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            for token in tokens:
                self.tokenTypes.get(token.type, self.noOp)(token)

    def checkName(self, token: TokenInfo):
        if token.string in self.reservedKeywords:
            self.pif.append((self.RESERVED_KEYWORD, token.string))
            return

        self.pif.append((self.FUNCTION_NAME, token.string))

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


def main():
    sc = Scanner()
    sc.parseFile("problem1.brr")


if __name__ == '__main__':
    main()
