#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.lexer import Lexer, LexerError
from src.parser import Parser, ParseError
from src.interpreter import Interpreter
from src.environment import AuroraRuntimeError

def run_source(source, output_fn=print):
    try:
        tokens = Lexer(source).tokenize()
        tree   = Parser(tokens).parse()
        Interpreter(output_fn=output_fn).run(tree)
    except (LexerError, ParseError, AuroraRuntimeError) as e:
        output_fn(str(e))
    except RecursionError:
        output_fn("Runtime Error: Maximum recursion depth exceeded")
    except Exception as e:
        output_fn(f"Internal Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python aurora.py <file.aur>")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path) as f:
            source = f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)
    run_source(source)

if __name__ == "__main__":
    main()
