"""
Lexer for Tunisian School Algorithm Language
Converts source code into tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Any


class TokenType(Enum):
    # Keywords
    ALGORITHME = auto()
    DEBUT = auto()
    FIN = auto()
    VARIABLES = auto()
    SI = auto()
    ALORS = auto()
    SINON = auto()
    FINSI = auto()
    POUR = auto()
    ALLANT = auto()
    DE = auto()
    A = auto()
    FAIRE = auto()
    FINPOUR = auto()
    TANTQUE = auto()
    FINTANTQUE = auto()
    REPETER = auto()
    JUSQUA = auto()
    ECRIRE = auto()
    LIRE = auto()
    
    # Data types
    ENTIER = auto()
    REEL = auto()
    CARACTERE = auto()
    CHAINE = auto()
    BOOLEEN = auto()
    TABLEAU = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MOD = auto()
    DIV = auto()
    ASSIGN = auto()
    
    # Comparison operators
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Logical operators
    ET = auto()
    OU = auto()
    NON = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    KEYWORDS = {
        'Algorithme': TokenType.ALGORITHME,
        'Debut': TokenType.DEBUT,
        'Fin': TokenType.FIN,
        'Variables': TokenType.VARIABLES,
        'Si': TokenType.SI,
        'Alors': TokenType.ALORS,
        'Sinon': TokenType.SINON,
        'FinSi': TokenType.FINSI,
        'Pour': TokenType.POUR,
        'allant': TokenType.ALLANT,
        'Faire': TokenType.FAIRE,
        'FinPour': TokenType.FINPOUR,
        'TantQue': TokenType.TANTQUE,
        'FinTantQue': TokenType.FINTANTQUE,
        'Repeter': TokenType.REPETER,
        'Répéter': TokenType.REPETER,
        "Jusqu'a": TokenType.JUSQUA,
        "Jusqu'à": TokenType.JUSQUA,
        'Ecrire': TokenType.ECRIRE,
        'Écrire': TokenType.ECRIRE,
        'Lire': TokenType.LIRE,
        'Entier': TokenType.ENTIER,
        'Reel': TokenType.REEL,
        'Réel': TokenType.REEL,
        'Caractere': TokenType.CARACTERE,
        'Caractère': TokenType.CARACTERE,
        'Chaine': TokenType.CHAINE,
        'Chaîne': TokenType.CHAINE,
        'Booleen': TokenType.BOOLEEN,
        'Booléen': TokenType.BOOLEEN,
        'Tableau': TokenType.TABLEAU,
        'Vrai': TokenType.BOOLEAN,
        'Faux': TokenType.BOOLEAN,
        'ET': TokenType.ET,
        'OU': TokenType.OU,
        'NON': TokenType.NON,
        'Mod': TokenType.MOD,
        'Div': TokenType.DIV,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source) and self.source[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_col)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        string_val = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\' and self.peek_char() == quote_char:
                self.advance()
                string_val += quote_char
                self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_col = self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() in "_'àâäéèêëïîôùûüÿœæçÀÂÄÉÈÊËÏÎÔÙÛÜŸŒÆÇ"):
            identifier += self.current_char()
            self.advance()
        
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        if token_type == TokenType.BOOLEAN:
            value = True if identifier == 'Vrai' else False
            return Token(token_type, value, start_line, start_col)
        
        return Token(token_type, identifier, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            # Newlines
            if self.current_char() == '\n':
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() in "ÉÀÂÄÈÊËÏÎÔÙÛÜéàâäèêëïîôùûü":
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and punctuation
            start_line = self.line
            start_col = self.column
            char = self.current_char()
            
            if char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
                self.advance()
            elif char == ':':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.ASSIGN, ':=', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
                    self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.EQUAL, '=', start_line, start_col))
                self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                elif self.peek_char() == '>':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT_EQUAL, '<>', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.LESS_THAN, '<', start_line, start_col))
                    self.advance()
            elif char == '>':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.GREATER_THAN, '>', start_line, start_col))
                    self.advance()
            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
