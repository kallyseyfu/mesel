from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Union

class NodeType(Enum):
    PROGRAM = 'PROGRAM'
    BLOCK = 'BLOCK'
    VARIABLE_DECLARATION = 'VARIABLE_DECLARATION'
    ASSIGNMENT = 'ASSIGNMENT'
    BINARY_OPERATION = 'BINARY_OPERATION'
    UNARY_OPERATION = 'UNARY_OPERATION'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'
    PRINT = 'PRINT'
    FOR_LOOP = 'FOR_LOOP'
    WHILE_LOOP = 'WHILE_LOOP'
    IF_STATEMENT = 'IF_STATEMENT'
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'
    TURTLE_COMMAND = 'TURTLE_COMMAND'
    COLOR_COMMAND = 'COLOR_COMMAND'
    WIDTH_COMMAND = 'WIDTH_COMMAND'

# Base node class
@dataclass
class Node:
    type: NodeType
    line: int
    column: int

# Expression nodes
@dataclass
class Expression(Node):
    pass

@dataclass
class Number(Expression):
    value: float

@dataclass
class String(Expression):
    value: str

@dataclass
class Boolean(Expression):
    value: bool

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class Input(Expression):
    prompt: Optional[Expression] = None

# Statement nodes
@dataclass
class Statement(Node):
    pass

@dataclass
class Program(Node):
    statements: List[Statement]

@dataclass
class Block(Statement):
    statements: List[Statement]

@dataclass
class Assignment(Statement):
    name: str
    value: Expression

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_block: Block
    else_block: Optional[Block] = None

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Block

@dataclass
class ForStatement(Statement):
    count: Expression
    body: Block

@dataclass
class PrintStatement(Statement):
    expression: Expression

@dataclass
class InputStatement(Statement):
    variable: str
    prompt: Optional[Expression] = None

# Turtle Graphics nodes
@dataclass
class Forward(Statement):
    distance: Expression

@dataclass
class Turn(Statement):
    angle: Expression

@dataclass
class PenDown(Statement):
    pass

@dataclass
class PenUp(Statement):
    pass

@dataclass
class ForLoop(Node):
    variable: Optional[str]
    start: Expression
    end: Expression
    body: Block

class ForLoop(Node):
    def __init__(self, variable: str, start: float, end: float, body: Block = None):
        super().__init__(NodeType.FOR_LOOP)
        self.variable = variable  # None for numeric range loops
        self.start = start
        self.end = end
        self.body = body or Block([]) 