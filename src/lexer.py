from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class TokenType(Enum):
    INTEGER = auto(); FLOAT = auto(); STRING = auto()
    TRUE = auto(); FALSE = auto(); NULL = auto()
    INT_TYPE = auto(); FLOAT_TYPE = auto(); STRING_TYPE = auto()
    BOOL_TYPE = auto(); LIST_TYPE = auto(); MAP_TYPE = auto(); AUTO = auto()
    IF = auto(); ELSE = auto(); WHILE = auto(); FOR = auto(); IN = auto()
    BREAK = auto(); RETURN = auto()
    FUNC = auto(); CLASS = auto(); IMPORT = auto(); MUT = auto(); PRINT = auto()
    IDENTIFIER = auto()
    PLUS = auto(); MINUS = auto(); STAR = auto(); SLASH = auto(); PERCENT = auto()
    EQUAL = auto(); COLON_EQUAL = auto()
    EQUAL_EQUAL = auto(); BANG_EQUAL = auto()
    LESS = auto(); LESS_EQUAL = auto(); GREATER = auto(); GREATER_EQUAL = auto()
    AND = auto(); OR = auto(); NOT = auto()
    ARROW = auto(); DOT_DOT = auto()
    SEMICOLON = auto(); COLON = auto(); COMMA = auto(); DOT = auto(); BANG = auto()
    LPAREN = auto(); RPAREN = auto()
    LBRACE = auto(); RBRACE = auto()
    LBRACKET = auto(); RBRACKET = auto()
    EOF = auto()

# Maps reserved keywords to their token types; anything else is an IDENTIFIER
KEYWORDS = {
    "print": TokenType.PRINT, "if": TokenType.IF, "else": TokenType.ELSE,
    "while": TokenType.WHILE, "for": TokenType.FOR, "in": TokenType.IN,
    "break": TokenType.BREAK, "return": TokenType.RETURN,
    "func": TokenType.FUNC, "class": TokenType.CLASS, "import": TokenType.IMPORT,
    "mut": TokenType.MUT, "auto": TokenType.AUTO,
    "true": TokenType.TRUE, "false": TokenType.FALSE, "null": TokenType.NULL,
    "and": TokenType.AND, "or": TokenType.OR, "not": TokenType.NOT,
    "Int": TokenType.INT_TYPE, "Float": TokenType.FLOAT_TYPE,
    "String": TokenType.STRING_TYPE, "Bool": TokenType.BOOL_TYPE,
    "List": TokenType.LIST_TYPE, "Map": TokenType.MAP_TYPE,
}

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    def __repr__(self): return f"{self.type.name}({self.value!r})"

class LexerError(Exception):
    def __init__(self, msg, line):
        super().__init__(f"[Line {line}] Lexer Error: {msg}")
        self.line = line

class Lexer:
    def __init__(self, source):
        self.source = source; self.pos = 0; self.line = 1

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self):
        p = self.pos + 1
        return self.source[p] if p < len(self.source) else None

    def advance(self):
        ch = self.source[self.pos]; self.pos += 1
        if ch == "\n": self.line += 1  # keep line count accurate for error messages
        return ch

    def skip(self):
        while self.current() is not None:
            if self.current() in " \t\r\n":
                self.advance()
            elif self.current() == "/" and self.peek() == "/":
                while self.current() and self.current() != "\n": self.advance()  # skip // comments
            else:
                break

    def read_number(self):
        ln = self.line; res = []
        while self.current() and self.current().isdigit(): res.append(self.advance())
        if self.current() == "." and self.peek() and self.peek().isdigit():
            res.append(self.advance())
            while self.current() and self.current().isdigit(): res.append(self.advance())
            return Token(TokenType.FLOAT, "".join(res), ln)
        return Token(TokenType.INTEGER, "".join(res), ln)

    def read_string(self):
        ln = self.line; self.advance(); res = []
        while self.current() and self.current() != '"':
            if self.current() == "\\":
                self.advance()
                esc = self.current()
                res.append({"n":"\n","t":"\t",'"':'"',"\\":"\\"}.get(esc, "\\"+esc))
                self.advance()
            else:
                res.append(self.advance())
        if self.current() is None: raise LexerError("Unterminated string", ln)
        self.advance()  # consume closing quote
        return Token(TokenType.STRING, "".join(res), ln)

    def read_ident(self):
        ln = self.line; res = []
        while self.current() and (self.current().isalnum() or self.current() == "_"):
            res.append(self.advance())
        word = "".join(res)
        return Token(KEYWORDS.get(word, TokenType.IDENTIFIER), word, ln)

    def tokenize(self):
        tokens = []
        while True:
            self.skip()
            ch = self.current()
            if ch is None:
                tokens.append(Token(TokenType.EOF, "EOF", self.line)); break
            ln = self.line
            if ch.isdigit(): tokens.append(self.read_number())
            elif ch == '"': tokens.append(self.read_string())
            elif ch.isalpha() or ch == "_": tokens.append(self.read_ident())
            elif ch == "+": self.advance(); tokens.append(Token(TokenType.PLUS,"+",ln))
            elif ch == "-":
                self.advance()
                if self.current() == ">": self.advance(); tokens.append(Token(TokenType.ARROW,"->",ln))
                else: tokens.append(Token(TokenType.MINUS,"-",ln))
            elif ch == "*": self.advance(); tokens.append(Token(TokenType.STAR,"*",ln))
            elif ch == "/": self.advance(); tokens.append(Token(TokenType.SLASH,"/",ln))
            elif ch == "%": self.advance(); tokens.append(Token(TokenType.PERCENT,"%",ln))
            elif ch == "=":
                self.advance()
                if self.current() == "=": self.advance(); tokens.append(Token(TokenType.EQUAL_EQUAL,"==",ln))
                else: tokens.append(Token(TokenType.EQUAL,"=",ln))
            elif ch == "!":
                self.advance()
                if self.current() == "=": self.advance(); tokens.append(Token(TokenType.BANG_EQUAL,"!=",ln))
                else: tokens.append(Token(TokenType.BANG,"!",ln))
            elif ch == "<":
                self.advance()
                if self.current() == "=": self.advance(); tokens.append(Token(TokenType.LESS_EQUAL,"<=",ln))
                else: tokens.append(Token(TokenType.LESS,"<",ln))
            elif ch == ">":
                self.advance()
                if self.current() == "=": self.advance(); tokens.append(Token(TokenType.GREATER_EQUAL,">=",ln))
                else: tokens.append(Token(TokenType.GREATER,">",ln))
            elif ch == ":":
                self.advance()
                if self.current() == "=": self.advance(); tokens.append(Token(TokenType.COLON_EQUAL,":=",ln))
                else: tokens.append(Token(TokenType.COLON,":",ln))
            elif ch == ".":
                self.advance()
                if self.current() == ".": self.advance(); tokens.append(Token(TokenType.DOT_DOT,"..",ln))
                else: tokens.append(Token(TokenType.DOT,".",ln))
            elif ch == ";": self.advance(); tokens.append(Token(TokenType.SEMICOLON,";",ln))
            elif ch == ",": self.advance(); tokens.append(Token(TokenType.COMMA,",",ln))
            elif ch == "(": self.advance(); tokens.append(Token(TokenType.LPAREN,"(",ln))
            elif ch == ")": self.advance(); tokens.append(Token(TokenType.RPAREN,")",ln))
            elif ch == "{": self.advance(); tokens.append(Token(TokenType.LBRACE,"{",ln))
            elif ch == "}": self.advance(); tokens.append(Token(TokenType.RBRACE,"}",ln))
            elif ch == "[": self.advance(); tokens.append(Token(TokenType.LBRACKET,"[",ln))
            elif ch == "]": self.advance(); tokens.append(Token(TokenType.RBRACKET,"]",ln))
            else: raise LexerError(f"Unknown character {ch!r}", self.line)
        return tokens
