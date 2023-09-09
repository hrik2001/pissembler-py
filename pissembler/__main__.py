from pissembler.lexer import Lexer, token_type

def main():
    lexer = Lexer([["PUSH1", token_type.PUSH1],["PUSH2", token_type.PUSH2], ["MSTORE", token_type.MSTORE], ["RETURN", token_type.RETURN]])
    print(lexer.lex("PUSH1 PUSH2    MSTORE"))

main()
