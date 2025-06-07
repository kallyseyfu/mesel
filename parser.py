from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from lexer import Token, TokenType
from ast_nodes import NodeType

@dataclass
class Node:
    type: NodeType
    line: int
    column: int

@dataclass
class Program(Node):
    statements: List['Statement']

@dataclass
class Block(Node):
    statements: List['Statement']

@dataclass
class Statement(Node):
    pass

@dataclass
class VariableDeclaration(Statement):
    name: str
    var_type: TokenType
    value: Optional['Expression']

@dataclass
class Assignment(Statement):
    name: str
    value: 'Expression'

@dataclass
class Expression(Node):
    pass

@dataclass
class BinaryOperation(Expression):
    left: Expression
    operator: TokenType
    right: Expression

@dataclass
class UnaryOperation(Expression):
    operator: TokenType
    operand: Expression

@dataclass
class Number(Expression):
    value: float

@dataclass
class String(Expression):
    value: str

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class Print(Statement):
    expression: Expression

@dataclass
class ForLoop(Statement):
    variable: Optional[str]
    start: Expression
    end: Expression
    body: Block

@dataclass
class WhileLoop(Statement):
    condition: Expression
    body: Block

@dataclass
class IfStatement(Statement):
    condition: Expression
    body: Block
    else_body: Optional[Block]

@dataclass
class Break(Statement):
    pass

@dataclass
class Continue(Statement):
    pass

@dataclass
class TurtleCommand(Statement):
    command: TokenType
    argument: Optional[Expression]

@dataclass
class ColorCommand(Statement):
    color: TokenType

@dataclass
class WidthCommand(Statement):
    width: Expression

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def error(self, message: str):
        token = self.tokens[self.current]
        raise Exception(f'Error at line {token.line}, column {token.column}: {message}')
    
    def peek(self) -> Token:
        if self.current >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        self.error(message)
    
    def program(self) -> Program:
        statements = []
        # Skip any leading newlines at the start of the file
        while self.check(TokenType.NEWLINE):
            self.advance()
        while not self.is_at_end():
            # Skip newlines
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            # Only parse a statement if the next token is a valid statement starter
            if self.check(TokenType.ASSIGN) or \
               self.check(TokenType.NUMBER_TYPE) or \
               self.check(TokenType.BEGIN) or \
               self.check(TokenType.FOR) or \
               self.check(TokenType.WHILE) or \
               self.check(TokenType.IF) or \
               self.check(TokenType.BREAK) or \
               self.check(TokenType.CONTINUE) or \
               self.check(TokenType.PRINT) or \
               self.check(TokenType.FORWARD) or \
               self.check(TokenType.TURN) or \
               self.check(TokenType.PEN_DOWN) or \
               self.check(TokenType.PEN_UP) or \
               self.check(TokenType.COLOR) or \
               self.check(TokenType.WIDTH):
                statements.append(self.statement())
            else:
                # Skip any unexpected tokens
                self.advance()
        return Program(NodeType.PROGRAM, 1, 1, statements)
    
    def statement(self) -> Statement:
        if self.match(TokenType.ASSIGN):
            name = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'አስቀምጥ'.").value
            self.consume(TokenType.ASSIGN_OP, "Expected '=' after variable name.")
            value = self.expression()
            return Assignment(NodeType.ASSIGNMENT, self.previous().line, self.previous().column, name, value)
            
        if self.match(TokenType.NUMBER_TYPE):
            name = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'ቁጥር'.").value
            self.consume(TokenType.ASSIGN_OP, "Expected '=' after variable name.")
            value = self.expression()
            return VariableDeclaration(NodeType.VARIABLE_DECLARATION, self.previous().line, 
                                     self.previous().column, name, TokenType.NUMBER_TYPE, value)
        
        if self.match(TokenType.BEGIN):
            return self.block()
        if self.match(TokenType.FOR):
            # For numeric range loops (እድግ 4)
            if self.check(TokenType.NUMBER):
                end = float(self.consume(TokenType.NUMBER, "Expected number for loop range.").value)
                body = self.block()
                return ForLoop(NodeType.FOR_LOOP, self.previous().line, self.previous().column,
                              None,  # No variable for numeric range
                              Number(NodeType.NUMBER, self.previous().line, self.previous().column, 0),  # Start at 0
                              Number(NodeType.NUMBER, self.previous().line, self.previous().column, end),  # End at specified number
                              body)
            # For variable-based loops (እድግ i = 1, 10)
            variable = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'እድግ'.").value
            self.consume(TokenType.ASSIGN_OP, "Expected '=' after variable name.")
            start = self.expression()
            self.consume(TokenType.COMMA, "Expected ',' after start value.")
            end = self.expression()
            body = self.block()
            return ForLoop(NodeType.FOR_LOOP, self.previous().line, self.previous().column,
                          variable, start, end, body)
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.CONTINUE):
            return self.continue_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.FORWARD, TokenType.TURN, TokenType.PEN_DOWN, TokenType.PEN_UP):
            return self.turtle_command()
        if self.match(TokenType.COLOR):
            return self.color_command()
        if self.match(TokenType.WIDTH):
            return self.width_command()
        
        # If we get here, we have an error
        token = self.peek()
        self.error(f"Expected statement, got {token.type} at line {token.line}, column {token.column}")
    
    def block(self) -> Block:
        statements = []
        while not self.check(TokenType.END) and not self.is_at_end():
            # Skip newlines and comments (if you have a comment token)
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            # Only parse a statement if the next token is a valid statement starter
            if self.check(TokenType.ASSIGN) or \
               self.check(TokenType.NUMBER_TYPE) or \
               self.check(TokenType.BEGIN) or \
               self.check(TokenType.FOR) or \
               self.check(TokenType.WHILE) or \
               self.check(TokenType.IF) or \
               self.check(TokenType.BREAK) or \
               self.check(TokenType.CONTINUE) or \
               self.check(TokenType.PRINT) or \
               self.check(TokenType.FORWARD) or \
               self.check(TokenType.TURN) or \
               self.check(TokenType.PEN_DOWN) or \
               self.check(TokenType.PEN_UP) or \
               self.check(TokenType.COLOR) or \
               self.check(TokenType.WIDTH):
                statements.append(self.statement())
            else:
                # Skip any unexpected tokens
                self.advance()
        # Skip any trailing newlines before END
        while self.check(TokenType.NEWLINE):
            self.advance()
        self.consume(TokenType.END, "Expected 'ጨርስ' after block.")
        return Block(NodeType.BLOCK, self.previous().line, self.previous().column, statements)
    
    def while_statement(self) -> WhileLoop:
        condition = self.expression()
        body = self.block()
        return WhileLoop(NodeType.WHILE_LOOP, self.previous().line, self.previous().column,
                        condition, body)
    
    def if_statement(self) -> IfStatement:
        condition = self.expression()
        body = self.block()
        else_body = None
        
        if self.match(TokenType.ELSE):
            else_body = self.block()
            
        return IfStatement(NodeType.IF_STATEMENT, self.previous().line, self.previous().column,
                          condition, body, else_body)
    
    def break_statement(self) -> Break:
        return Break(NodeType.BREAK, self.previous().line, self.previous().column)
    
    def continue_statement(self) -> Continue:
        return Continue(NodeType.CONTINUE, self.previous().line, self.previous().column)
    
    def print_statement(self) -> Print:
        value = self.expression()
        return Print(NodeType.PRINT, self.previous().line, self.previous().column, value)
    
    def turtle_command(self) -> TurtleCommand:
        command = self.previous().type
        argument = None
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.END):
            argument = self.expression()
        return TurtleCommand(NodeType.TURTLE_COMMAND, self.previous().line, self.previous().column,
                           command, argument)
    
    def color_command(self) -> ColorCommand:
        # Check for any color token
        if self.match(TokenType.RED, TokenType.GREEN, TokenType.BLUE, 
                     TokenType.YELLOW, TokenType.BLACK, TokenType.WHITE):
            color = self.previous().type
            return ColorCommand(NodeType.COLOR_COMMAND, self.previous().line, self.previous().column, color)
        self.error("Expected color after 'ቀለም'.")
    
    def width_command(self) -> WidthCommand:
        width = self.expression()
        return WidthCommand(NodeType.WIDTH_COMMAND, self.previous().line, self.previous().column, width)
    
    def expression_statement(self) -> Statement:
        expr = self.expression()
        if isinstance(expr, Identifier) and self.match(TokenType.ASSIGN_OP):
            value = self.expression()
            return Assignment(NodeType.ASSIGNMENT, expr.line, expr.column, expr.name, value)
        return expr
    
    def expression(self) -> Expression:
        return self.equality()
    
    def equality(self) -> Expression:
        expr = self.comparison()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.previous().type
            right = self.comparison()
            expr = BinaryOperation(NodeType.BINARY_OPERATION, expr.line, expr.column,
                                 expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expression:
        expr = self.term()
        
        while self.match(TokenType.GREATER, TokenType.LESS, 
                        TokenType.GREATER_EQUALS, TokenType.LESS_EQUALS):
            operator = self.previous().type
            right = self.term()
            expr = BinaryOperation(NodeType.BINARY_OPERATION, expr.line, expr.column,
                                 expr, operator, right)
        
        return expr
    
    def term(self) -> Expression:
        expr = self.factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().type
            right = self.factor()
            expr = BinaryOperation(NodeType.BINARY_OPERATION, expr.line, expr.column,
                                 expr, operator, right)
        
        return expr
    
    def factor(self) -> Expression:
        expr = self.power()
        
        while self.match(TokenType.TIMES, TokenType.DIVIDE_OP, TokenType.MODULO_OP):
            operator = self.previous().type
            right = self.power()
            expr = BinaryOperation(NodeType.BINARY_OPERATION, expr.line, expr.column,
                                 expr, operator, right)
        
        return expr
    
    def power(self) -> Expression:
        expr = self.unary()
        
        if self.match(TokenType.POWER_OP):
            operator = self.previous().type
            right = self.unary()
            expr = BinaryOperation(NodeType.BINARY_OPERATION, expr.line, expr.column,
                                 expr, operator, right)
        
        return expr
    
    def unary(self) -> Expression:
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous().type
            right = self.unary()
            return UnaryOperation(NodeType.UNARY_OPERATION, self.previous().line, 
                                self.previous().column, operator, right)
        
        return self.primary()
    
    def primary(self) -> Expression:
        if self.match(TokenType.NUMBER):
            return Number(NodeType.NUMBER, self.previous().line, self.previous().column,
                         float(self.previous().value))
        
        if self.match(TokenType.STRING):
            return String(NodeType.STRING, self.previous().line, self.previous().column,
                         self.previous().value)
        
        if self.match(TokenType.IDENTIFIER):
            return Identifier(NodeType.IDENTIFIER, self.previous().line, self.previous().column,
                            self.previous().value)
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr
        
        # If we get here, we have an error
        token = self.peek()
        self.error(f"Expected expression, got {token.type} at line {token.line}, column {token.column}")
    
    def parse(self) -> Program:
        return self.program()
