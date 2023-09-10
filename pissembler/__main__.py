from pissembler.lexer import lexer
import sys
from pprint import pprint

def main():
    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".piss"):
            pprint(lexer.lex(open(sys.argv[1]).read()))
            exit()
        else:
            raise Exception(f"Wrong file type {sys.argv[1]}")

    # Basic shell implementation :P
    while True:
        pprint(lexer.lex(input(">")))

main()
