"""
Interpreter for Tunisian School Algorithm Language
Executes the Abstract Syntax Tree (AST)
"""

from typing import Any, Dict, List
from parser import *


class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []
    
    def execute(self, program: Program) -> List[str]:
        # Initialize variables
        for var_decl in program.variables:
            if var_decl.is_array:
                self.variables[var_decl.name] = [None] * var_decl.array_size
            else:
                self.variables[var_decl.name] = self.get_default_value(var_decl.var_type)
        
        # Execute body
        for statement in program.body:
            self.execute_statement(statement)
        
        return self.output
    
    def get_default_value(self, var_type: str) -> Any:
        type_map = {
            'Entier': 0,
            'Reel': 0.0,
            'Réel': 0.0,
            'Caractere': '',
            'Caractère': '',
            'Chaine': '',
            'Chaîne': '',
            'Booleen': False,
            'Booléen': False,
        }
        return type_map.get(var_type, None)
    
    def execute_statement(self, statement: ASTNode):
        if isinstance(statement, Assignment):
            self.execute_assignment(statement)
        elif isinstance(statement, IfStatement):
            self.execute_if_statement(statement)
        elif isinstance(statement, ForLoop):
            self.execute_for_loop(statement)
        elif isinstance(statement, WhileLoop):
            self.execute_while_loop(statement)
        elif isinstance(statement, RepeatLoop):
            self.execute_repeat_loop(statement)
        elif isinstance(statement, WriteStatement):
            self.execute_write_statement(statement)
        elif isinstance(statement, ReadStatement):
            self.execute_read_statement(statement)
    
    def execute_assignment(self, statement: Assignment):
        value = self.evaluate_expression(statement.value)
        
        if statement.index is not None:
            # Array assignment
            index = self.evaluate_expression(statement.index)
            if not isinstance(index, int):
                raise RuntimeError(f"Array index must be an integer, got {type(index)}")
            
            if statement.target not in self.variables:
                raise RuntimeError(f"Variable '{statement.target}' not declared")
            
            array = self.variables[statement.target]
            if not isinstance(array, list):
                raise RuntimeError(f"Variable '{statement.target}' is not an array")
            
            if index < 0 or index >= len(array):
                raise RuntimeError(f"Array index {index} out of bounds for '{statement.target}'")
            
            array[index] = value
        else:
            # Simple assignment
            self.variables[statement.target] = value
    
    def execute_if_statement(self, statement: IfStatement):
        condition = self.evaluate_expression(statement.condition)
        
        if condition:
            for stmt in statement.then_branch:
                self.execute_statement(stmt)
        elif statement.else_branch:
            for stmt in statement.else_branch:
                self.execute_statement(stmt)
    
    def execute_for_loop(self, statement: ForLoop):
        start = self.evaluate_expression(statement.start)
        end = self.evaluate_expression(statement.end)
        
        if not isinstance(start, int) or not isinstance(end, int):
            raise RuntimeError("For loop bounds must be integers")
        
        for i in range(start, end + 1):
            self.variables[statement.variable] = i
            for stmt in statement.body:
                self.execute_statement(stmt)
    
    def execute_while_loop(self, statement: WhileLoop):
        while self.evaluate_expression(statement.condition):
            for stmt in statement.body:
                self.execute_statement(stmt)
    
    def execute_repeat_loop(self, statement: RepeatLoop):
        while True:
            for stmt in statement.body:
                self.execute_statement(stmt)
            
            if self.evaluate_expression(statement.condition):
                break
    
    def execute_write_statement(self, statement: WriteStatement):
        values = []
        for expr in statement.expressions:
            value = self.evaluate_expression(expr)
            values.append(str(value))
        
        output_line = ' '.join(values)
        self.output.append(output_line)
        print(output_line)
    
    def execute_read_statement(self, statement: ReadStatement):
        for var_name in statement.variables:
            if var_name not in self.variables:
                raise RuntimeError(f"Variable '{var_name}' not declared")
            
            user_input = input(f"Enter value for {var_name}: ")
            
            # Try to convert to appropriate type
            try:
                # Try integer first
                value = int(user_input)
            except ValueError:
                try:
                    # Try float
                    value = float(user_input)
                except ValueError:
                    # Keep as string
                    value = user_input
            
            self.variables[var_name] = value
    
    def evaluate_expression(self, expr: ASTNode) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Identifier):
            if expr.name not in self.variables:
                raise RuntimeError(f"Variable '{expr.name}' not declared")
            
            if expr.index is not None:
                # Array access
                index = self.evaluate_expression(expr.index)
                if not isinstance(index, int):
                    raise RuntimeError(f"Array index must be an integer, got {type(index)}")
                
                array = self.variables[expr.name]
                if not isinstance(array, list):
                    raise RuntimeError(f"Variable '{expr.name}' is not an array")
                
                if index < 0 or index >= len(array):
                    raise RuntimeError(f"Array index {index} out of bounds for '{expr.name}'")
                
                return array[index]
            else:
                return self.variables[expr.name]
        elif isinstance(expr, BinaryOp):
            return self.evaluate_binary_op(expr)
        elif isinstance(expr, UnaryOp):
            return self.evaluate_unary_op(expr)
        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")
    
    def evaluate_binary_op(self, expr: BinaryOp) -> Any:
        left = self.evaluate_expression(expr.left)
        right = self.evaluate_expression(expr.right)
        op = expr.operator
        
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif op == 'Div':
            if right == 0:
                raise RuntimeError("Division by zero")
            return int(left // right)
        elif op == 'Mod':
            if right == 0:
                raise RuntimeError("Modulo by zero")
            return left % right
        elif op == '=':
            return left == right
        elif op == '<>':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == 'ET':
            return bool(left) and bool(right)
        elif op == 'OU':
            return bool(left) or bool(right)
        else:
            raise RuntimeError(f"Unknown operator: {op}")
    
    def evaluate_unary_op(self, expr: UnaryOp) -> Any:
        operand = self.evaluate_expression(expr.operand)
        op = expr.operator
        
        if op == '-':
            return -operand
        elif op == 'NON':
            return not bool(operand)
        else:
            raise RuntimeError(f"Unknown unary operator: {op}")
