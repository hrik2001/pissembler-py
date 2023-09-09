'''
Here, grammar of the pissembler language is defined
'''

# from pissembler.lexer import token_type
from enum import Enum, auto
import re

class pissembler_token_type(Enum):
    PUSH1 = auto()
    PUSH2 = auto()
    MSTORE = auto()
    RETURN = auto()
    HEX_LITERAL = auto()
    DECIMAL_LITERAL = auto()

instructions = [
    ["PUSH1", pissembler_token_type.PUSH1],
    ["PUSH2", pissembler_token_type.PUSH2],
    ["MSTORE", pissembler_token_type.MSTORE],
    ["RETURN", pissembler_token_type.RETURN]
]


literal_rules = {
    pissembler_token_type.DECIMAL_LITERAL: re.compile(r"[0-9]+"),
    pissembler_token_type.HEX_LITERAL: re.compile(r"0x(([0-9])|([A-Z])|([a-z]))+")
}
