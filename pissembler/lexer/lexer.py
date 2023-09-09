from enum import Enum, auto
from typing import List, Optional
from pydantic import BaseModel
import re

class token_type(Enum):
    PUSH1 = auto()
    PUSH2 = auto()
    MSTORE = auto()
    RETURN = auto()
    HEX_LITERAL = auto()
    DECIMAL_LITERAL = auto()

class Token(BaseModel):
    t_type: token_type
    value: Optional[str] = None

class LexerEdge(BaseModel):
    value: Optional[str]
    is_start: bool = False
    t_type: Optional[token_type] = None # will contain a value only when is_end = True
    next_edges: List["LexerEdge"] = []

class Lexer:
    def __init__(self, instructions):
        '''
        instructions contain any instruction that is not hex or decimal
        it's a list of ["INSTRUCTION", token_type.INSTRUCTION]
        for example: [["PUSH1", token_type.PUSH1], ["MSTORE", token_type.MSTORE], ["RETURN", token_type.RETURN]]

        Here in intialization we build the state machine :)
        '''
        self.state = LexerEdge(value=None, is_start=True)
        for instruction, instruction_enum in instructions:
            curr = self.state
            length = len(instruction)
            for index, character in enumerate(instruction):
                skip = False
                is_end = (index == (length - 1))
                for edge in curr.next_edges:
                    if edge.value == character:
                        curr = edge
                        skip = True
                        break
                if skip:
                    continue
                next_edge = LexerEdge(value=character, t_type=(instruction_enum if is_end else None))
                curr.next_edges.append(next_edge)
                curr = next_edge

    def lex(self, text):
        curr = self.state
        result = []
        length = len(text)
        operand = {"value": None, "type": None}
        literal_rules = {
            token_type.DECIMAL_LITERAL: re.compile(r"[0-9]+"),
            token_type.HEX_LITERAL: re.compile(r"0x(([0-9])|([A-Z])|([a-z]))+")
        }
        index = 0
        # for index, character in enumerate(text):
        while index < length:
            character = text[index]
            change = False
            is_end = (index == (length - 1))
            if character.isspace():
                if not curr.is_start:
                    if curr.t_type is None:
                        raise Exception(f"Incomplete symbol at position {index+1}")
                    result.append(Token(t_type=curr.t_type))
                    curr = self.state
                index += 1
                continue

            for edge in curr.next_edges:
                if edge.value == character:
                    curr = edge
                    change = True
                    break
            if is_end and (not character.isspace()):
                # if operand["value"] is not None:
                    # result.append(Token(t_type=operand["type"], value=operand["value"]))
                    # break
                result.append(Token(t_type=curr.t_type))
                curr = self.state

            if not change:
                rest = text[index:]
                possibilities = []
                for literal_type in literal_rules.keys():
                    match_object = literal_rules[literal_type].match(rest)
                    if bool(match_object) and match_object.span()[0] == 0:
                        possibilities.append([literal_type, match_object.span()[1], match_object.group()])
                possibilities = sorted(possibilities, key=(lambda x: x[1]))[::-1]
                result.append(Token(t_type=possibilities[0][0], value=possibilities[0][2]))
                index += possibilities[0][1]
                change = True


            if not change:
                raise Exception(f"Unsupported symbol probably at position {index+1}")
            index += 1
        return result
