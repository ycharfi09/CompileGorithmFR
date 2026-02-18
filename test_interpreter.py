#!/usr/bin/env python3
"""
Test suite for CompileGorithmFR
Tests the lexer, parser, and interpreter
"""

import sys
from io import StringIO
from lexer import Lexer, TokenType
from parser import Parser
from interpreter import Interpreter


def test_lexer_basic():
    """Test basic tokenization"""
    source = "Algorithme Test\nVariables\nx: Entier\nDebut\nx := 5\nFin"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.ALGORITHME
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "Test"
    print("✓ Lexer basic test passed")


def test_lexer_operators():
    """Test operator tokenization"""
    source = "x := 5 + 3 * 2 - 1 / 2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    token_types = [t.type for t in tokens]
    assert TokenType.ASSIGN in token_types
    assert TokenType.PLUS in token_types
    assert TokenType.MULTIPLY in token_types
    assert TokenType.MINUS in token_types
    assert TokenType.DIVIDE in token_types
    print("✓ Lexer operators test passed")


def test_lexer_comparison():
    """Test comparison operators"""
    source = "Si x = 5 ET y <> 3 OU z >= 10 Alors"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    token_types = [t.type for t in tokens]
    assert TokenType.SI in token_types
    assert TokenType.EQUAL in token_types
    assert TokenType.ET in token_types
    assert TokenType.NOT_EQUAL in token_types
    assert TokenType.OU in token_types
    assert TokenType.GREATER_EQUAL in token_types
    print("✓ Lexer comparison test passed")


def test_parser_simple_program():
    """Test parsing a simple program"""
    source = """Algorithme Test
Variables
    x: Entier
Debut
    x := 10
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert ast.name == "Test"
    assert len(ast.variables) == 1
    assert ast.variables[0].name == "x"
    assert len(ast.body) == 1
    print("✓ Parser simple program test passed")


def test_parser_for_loop():
    """Test parsing for loops"""
    source = """Algorithme Test
Variables
    i: Entier
Debut
    Pour i allant de 1 a 10 Faire
        Ecrire(i)
    FinPour
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.body) == 1
    from parser import ForLoop
    assert isinstance(ast.body[0], ForLoop)
    print("✓ Parser for loop test passed")


def test_parser_if_statement():
    """Test parsing if statements"""
    source = """Algorithme Test
Variables
    x: Entier
Debut
    Si x > 5 Alors
        Ecrire("Grand")
    Sinon
        Ecrire("Petit")
    FinSi
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    from parser import IfStatement
    assert isinstance(ast.body[0], IfStatement)
    assert ast.body[0].else_branch is not None
    print("✓ Parser if statement test passed")


def test_interpreter_arithmetic():
    """Test arithmetic operations"""
    source = """Algorithme Test
Variables
    a, b, c: Entier
Debut
    a := 10
    b := 5
    c := a + b * 2
    Ecrire(c)
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    interpreter = Interpreter()
    interpreter.execute(ast)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "20" in output
    print("✓ Interpreter arithmetic test passed")


def test_interpreter_for_loop():
    """Test for loop execution"""
    source = """Algorithme Test
Variables
    i, sum: Entier
Debut
    sum := 0
    Pour i allant de 1 a 5 Faire
        sum := sum + i
    FinPour
    Ecrire(sum)
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    interpreter = Interpreter()
    interpreter.execute(ast)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "15" in output  # 1+2+3+4+5 = 15
    print("✓ Interpreter for loop test passed")


def test_interpreter_if_statement():
    """Test if statement execution"""
    source = """Algorithme Test
Variables
    x: Entier
Debut
    x := 10
    Si x > 5 Alors
        Ecrire("Pass")
    Sinon
        Ecrire("Fail")
    FinSi
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    interpreter = Interpreter()
    interpreter.execute(ast)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Pass" in output
    print("✓ Interpreter if statement test passed")


def test_interpreter_array():
    """Test array operations"""
    source = """Algorithme Test
Variables
    arr: Tableau[3] de Entier
    i: Entier
Debut
    arr[0] := 10
    arr[1] := 20
    arr[2] := 30
    Ecrire(arr[1])
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    interpreter = Interpreter()
    interpreter.execute(ast)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "20" in output
    print("✓ Interpreter array test passed")


def test_interpreter_boolean():
    """Test boolean operations"""
    source = """Algorithme Test
Variables
    a, b: Booleen
    result: Booleen
Debut
    a := Vrai
    b := Faux
    result := a ET NON b
    Si result Alors
        Ecrire("Success")
    FinSi
Fin"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    interpreter = Interpreter()
    interpreter.execute(ast)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Success" in output
    print("✓ Interpreter boolean test passed")


def run_all_tests():
    """Run all tests"""
    print("Running CompileGorithmFR tests...\n")
    
    tests = [
        test_lexer_basic,
        test_lexer_operators,
        test_lexer_comparison,
        test_parser_simple_program,
        test_parser_for_loop,
        test_parser_if_statement,
        test_interpreter_arithmetic,
        test_interpreter_for_loop,
        test_interpreter_if_statement,
        test_interpreter_array,
        test_interpreter_boolean,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
