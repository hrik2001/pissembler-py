from enum import Enum, auto
from typing import List, Optional
from pydantic import BaseModel

class token_type(Enum):
    PUSH1 = auto()
    PUSH2 = auto()
    MSTORE = auto()
    RETURN = auto()
    HEX_LITERAL = auto()
    DECIMAL_LITERAL = auto()

class Token(BaseModel):
    t_type: token_type
    value: str

class LexerEdge(BaseModel):
    value: Optional[str]
    is_start: bool = False
    t_type: token_type = None # will contain a value only when is_end = True
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
            prev = None
            length = len(instruction)
            for index, character in enumerate(instruction):
                skip = False
                is_end = (index == (length - 1))
                for edge in curr.next_edges:
                    if edge.value == character:
                        curr = edge
                        # print(character)
                        skip = True
                        break
                if skip:
                    continue
                next_edge = LexerEdge(value=character, t_type=(instruction_enum if is_end else None))
                # print(f"{character} (created)")
                curr.next_edges.append(next_edge)
                curr = next_edge

    def lex(self, text):
        curr = self.state
        result = []
        length = len(text)
        for index, character in enumerate(text):
            change = False
            is_end = (index == (length - 1))
            if character.isspace():
                if not curr.is_start:
                    if curr.t_type is None:
                        raise Exception(f"Incomplete symbol at position {index+1}")
                    result.append(curr.t_type)
                    curr = self.state
                continue
            for edge in curr.next_edges:
                if edge.value == character:
                    curr = edge
                    change = True
                    break
            if is_end and (not character.isspace()):
                    result.append(curr.t_type)
                    curr = self.state
            if not change:
                raise Exception(f"Unsupported symbol probably at position {index+1}")
        return result
