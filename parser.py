"""
Parser for Tunisian School Algorithm Language
Converts tokens into an Abstract Syntax Tree (AST)
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from lexer import Token, TokenType, Lexer


# AST Node Classes
@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    name: str
    variables: List['VariableDecl']
    body: List[ASTNode]


@dataclass
class VariableDecl(ASTNode):
    name: str
    var_type: str
    is_array: bool = False
    array_size: Optional[int] = None


@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode
    index: Optional[ASTNode] = None


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class Literal(ASTNode):
    value: Any
    lit_type: str


@dataclass
class Identifier(ASTNode):
    name: str
    index: Optional[ASTNode] = None


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None


@dataclass
class ForLoop(ASTNode):
    variable: str
    start: ASTNode
    end: ASTNode
    body: List[ASTNode]


@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class RepeatLoop(ASTNode):
    body: List[ASTNode]
    condition: ASTNode


@dataclass
class WriteStatement(ASTNode):
    expressions: List[ASTNode]


@dataclass
class ReadStatement(ASTNode):
    variables: List[str]


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # Return EOF
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # Return EOF
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        self.skip_newlines()
        
        # Parse algorithm header
        self.expect(TokenType.ALGORITHME)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        self.skip_newlines()
        
        # Parse variables section
        variables = []
        if self.current_token().type == TokenType.VARIABLES:
            self.advance()
            self.skip_newlines()
            variables = self.parse_variables()
        
        # Parse body
        self.skip_newlines()
        self.expect(TokenType.DEBUT)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.FIN:
            self.skip_newlines()
            if self.current_token().type == TokenType.FIN:
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.FIN)
        
        return Program(name, variables, body)
    
    def parse_variables(self) -> List[VariableDecl]:
        variables = []
        
        while self.current_token().type == TokenType.IDENTIFIER:
            var_names = [self.current_token().value]
            self.advance()
            
            # Check for multiple variables of same type
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                var_names.append(self.expect(TokenType.IDENTIFIER).value)
            
            self.expect(TokenType.COLON)
            
            # Check for array
            is_array = False
            array_size = None
            if self.current_token().type == TokenType.TABLEAU:
                is_array = True
                self.advance()
                self.expect(TokenType.LBRACKET)
                size_token = self.expect(TokenType.INTEGER)
                array_size = size_token.value
                self.expect(TokenType.RBRACKET)
                # Expect 'de' as identifier
                de_token = self.expect(TokenType.IDENTIFIER)
                if de_token.value not in ['de']:
                    raise SyntaxError(f"Expected 'de', got '{de_token.value}' at line {de_token.line}")
            
            # Get type
            type_token = self.current_token()
            if type_token.type in [TokenType.ENTIER, TokenType.REEL, TokenType.CARACTERE, 
                                   TokenType.CHAINE, TokenType.BOOLEEN]:
                var_type = type_token.value
                self.advance()
            else:
                raise SyntaxError(f"Expected type, got {type_token.type} at line {type_token.line}")
            
            # Create variable declarations
            for var_name in var_names:
                variables.append(VariableDecl(var_name, var_type, is_array, array_size))
            
            self.skip_newlines()
        
        return variables
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.current_token()
        
        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        elif token.type == TokenType.SI:
            return self.parse_if_statement()
        elif token.type == TokenType.POUR:
            return self.parse_for_loop()
        elif token.type == TokenType.TANTQUE:
            return self.parse_while_loop()
        elif token.type == TokenType.REPETER:
            return self.parse_repeat_loop()
        elif token.type == TokenType.ECRIRE:
            return self.parse_write_statement()
        elif token.type == TokenType.LIRE:
            return self.parse_read_statement()
        elif token.type == TokenType.NEWLINE:
            self.advance()
            return None
        else:
            return None
    
    def parse_assignment(self) -> Assignment:
        target = self.current_token().value
        self.advance()
        
        # Check for array index
        index = None
        if self.current_token().type == TokenType.LBRACKET:
            self.advance()
            index = self.parse_expression()
            self.expect(TokenType.RBRACKET)
        
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        
        return Assignment(target, value, index)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.SI)
        condition = self.parse_expression()
        self.expect(TokenType.ALORS)
        self.skip_newlines()
        
        then_branch = []
        while self.current_token().type not in [TokenType.SINON, TokenType.FINSI]:
            self.skip_newlines()
            if self.current_token().type in [TokenType.SINON, TokenType.FINSI]:
                break
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
        
        else_branch = None
        if self.current_token().type == TokenType.SINON:
            self.advance()
            self.skip_newlines()
            else_branch = []
            while self.current_token().type != TokenType.FINSI:
                self.skip_newlines()
                if self.current_token().type == TokenType.FINSI:
                    break
                stmt = self.parse_statement()
                if stmt:
                    else_branch.append(stmt)
        
        self.expect(TokenType.FINSI)
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_for_loop(self) -> ForLoop:
        self.expect(TokenType.POUR)
        variable = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ALLANT)
        # Expect 'de' as identifier
        de_token = self.expect(TokenType.IDENTIFIER)
        if de_token.value not in ['de']:
            raise SyntaxError(f"Expected 'de', got '{de_token.value}' at line {de_token.line}")
        start = self.parse_expression()
        # Expect 'a' or 'à' as identifier
        a_token = self.expect(TokenType.IDENTIFIER)
        if a_token.value not in ['a', 'à']:
            raise SyntaxError(f"Expected 'a' or 'à', got '{a_token.value}' at line {a_token.line}")
        end = self.parse_expression()
        self.expect(TokenType.FAIRE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.FINPOUR:
            self.skip_newlines()
            if self.current_token().type == TokenType.FINPOUR:
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.FINPOUR)
        
        return ForLoop(variable, start, end, body)
    
    def parse_while_loop(self) -> WhileLoop:
        self.expect(TokenType.TANTQUE)
        condition = self.parse_expression()
        self.expect(TokenType.FAIRE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.FINTANTQUE:
            self.skip_newlines()
            if self.current_token().type == TokenType.FINTANTQUE:
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.FINTANTQUE)
        
        return WhileLoop(condition, body)
    
    def parse_repeat_loop(self) -> RepeatLoop:
        self.expect(TokenType.REPETER)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.JUSQUA:
            self.skip_newlines()
            if self.current_token().type == TokenType.JUSQUA:
                break
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.JUSQUA)
        condition = self.parse_expression()
        
        return RepeatLoop(body, condition)
    
    def parse_write_statement(self) -> WriteStatement:
        self.expect(TokenType.ECRIRE)
        self.expect(TokenType.LPAREN)
        
        expressions = []
        expressions.append(self.parse_expression())
        
        while self.current_token().type == TokenType.COMMA:
            self.advance()
            expressions.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        
        return WriteStatement(expressions)
    
    def parse_read_statement(self) -> ReadStatement:
        self.expect(TokenType.LIRE)
        self.expect(TokenType.LPAREN)
        
        variables = []
        variables.append(self.expect(TokenType.IDENTIFIER).value)
        
        while self.current_token().type == TokenType.COMMA:
            self.advance()
            variables.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.RPAREN)
        
        return ReadStatement(variables)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        
        while self.current_token().type == TokenType.OU:
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, 'OU', right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_logical_not()
        
        while self.current_token().type == TokenType.ET:
            self.advance()
            right = self.parse_logical_not()
            left = BinaryOp(left, 'ET', right)
        
        return left
    
    def parse_logical_not(self) -> ASTNode:
        if self.current_token().type == TokenType.NON:
            self.advance()
            operand = self.parse_logical_not()
            return UnaryOp('NON', operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        token = self.current_token()
        if token.type in [TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS_THAN, 
                         TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]:
            op = token.value
            self.advance()
            right = self.parse_additive()
            return BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, 
                                            TokenType.MOD, TokenType.DIV]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return UnaryOp('-', operand)
        elif token.type == TokenType.PLUS:
            self.advance()
            return self.parse_unary()
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.INTEGER:
            self.advance()
            return Literal(token.value, 'int')
        elif token.type == TokenType.FLOAT:
            self.advance()
            return Literal(token.value, 'float')
        elif token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value, 'string')
        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return Literal(token.value, 'bool')
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            # Check for array index
            if self.current_token().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return Identifier(name, index)
            
            return Identifier(name)
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")
