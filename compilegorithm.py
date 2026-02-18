#!/usr/bin/env python3
"""
CompileGorithmFR - Tunisian School Algorithm Language Interpreter
Main CLI interface for running algorithm files
"""

import sys
import argparse
from pathlib import Path
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_algorithm(source_code: str, debug: bool = False):
    """Run algorithm from source code"""
    try:
        # Lexical analysis
        if debug:
            print("=== Lexing ===")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        if debug:
            print(f"Tokens: {len(tokens)}")
            for token in tokens[:20]:  # Show first 20 tokens
                print(f"  {token}")
            if len(tokens) > 20:
                print(f"  ... and {len(tokens) - 20} more")
            print()
        
        # Parsing
        if debug:
            print("=== Parsing ===")
        parser = Parser(tokens)
        ast = parser.parse()
        
        if debug:
            print(f"Program: {ast.name}")
            print(f"Variables: {len(ast.variables)}")
            for var in ast.variables:
                print(f"  {var}")
            print(f"Statements: {len(ast.body)}")
            print()
        
        # Interpretation
        if debug:
            print("=== Executing ===")
        interpreter = Interpreter()
        output = interpreter.execute(ast)
        
        if debug:
            print("\n=== Program Output ===")
        
        return True, output
    
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        return False, []
    except RuntimeError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        return False, []
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if debug:
            import traceback
            traceback.print_exc()
        return False, []


def main():
    parser = argparse.ArgumentParser(
        description='CompileGorithmFR - Run Tunisian school algorithm language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s algorithm.algo                  # Run an algorithm file
  %(prog)s algorithm.algo --debug          # Run with debug output
  %(prog)s --example                       # Show example algorithm
        """
    )
    
    parser.add_argument('file', nargs='?', help='Algorithm file to run (.algo)')
    parser.add_argument('--debug', '-d', action='store_true', 
                       help='Enable debug output')
    parser.add_argument('--example', '-e', action='store_true',
                       help='Show an example algorithm')
    
    args = parser.parse_args()
    
    if args.example:
        example = """Algorithme ExempleSimple
Variables
    x, y, somme: Entier
    message: Chaine
Debut
    x := 10
    y := 20
    somme := x + y
    message := "La somme est:"
    Ecrire(message, somme)
Fin"""
        print(example)
        return 0
    
    if not args.file:
        parser.print_help()
        return 1
    
    # Read the algorithm file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1
    
    try:
        source_code = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1
    
    # Run the algorithm
    success, output = run_algorithm(source_code, args.debug)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
