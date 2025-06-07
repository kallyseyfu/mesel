from ast_nodes import *
from typing import List, Dict, Any
from parser import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code = []
        self.imports = set(['turtle', 'math'])
        self.variables = set()
    
    def generate(self, node: Node) -> str:
        if isinstance(node, Program):
            return self.generate_program(node)
        elif isinstance(node, Block):
            return self.generate_block(node)
        elif isinstance(node, VariableDeclaration):
            return self.generate_variable_declaration(node)
        elif isinstance(node, Assignment):
            return self.generate_assignment(node)
        elif isinstance(node, BinaryOperation):
            return self.generate_binary_operation(node)
        elif isinstance(node, UnaryOperation):
            return self.generate_unary_operation(node)
        elif isinstance(node, Number):
            return self.generate_number(node)
        elif isinstance(node, String):
            return self.generate_string(node)
        elif isinstance(node, Identifier):
            return self.generate_identifier(node)
        elif isinstance(node, Print):
            return self.generate_print(node)
        elif isinstance(node, ForLoop):
            return self.generate_for_loop(node)
        elif isinstance(node, WhileLoop):
            return self.generate_while_loop(node)
        elif isinstance(node, IfStatement):
            return self.generate_if_statement(node)
        elif isinstance(node, Break):
            return self.generate_break(node)
        elif isinstance(node, Continue):
            return self.generate_continue(node)
        elif isinstance(node, TurtleCommand):
            return self.generate_turtle_command(node)
        elif isinstance(node, ColorCommand):
            return self.generate_color_command(node)
        elif isinstance(node, WidthCommand):
            return self.generate_width_command(node)
        else:
            raise Exception(f"Unknown node type: {type(node)}")
    
    def generate_program(self, node: Program) -> str:
        code = [
            "import turtle",
            "def main():",
            "    screen = turtle.Screen()",
            "    screen.setup(800, 600)",  # Set window size
            "    screen.title('Mesel Turtle Graphics')",
            "    screen.bgcolor('white')",  # Set white background
            "    screen.tracer(0)",  # Turn off animation for faster drawing
            "    t = turtle.Turtle()",
            "    t.speed(0)",  # Fastest speed
            "    t.pensize(2)",  # Thicker lines
            "    t.color('blue')",  # Blue color for the flower
            "    t.penup()",  # Lift pen to move to starting position
            "    t.goto(0, 0)",  # Center of screen
            "    t.pendown()",  # Put pen down to start drawing
            "    try:"
        ]
        # Generate statements with proper indentation inside try block
        for statement in node.statements:
            stmt_code = self.generate(statement)
            if stmt_code:
                # Split into lines and indent each line with 8 spaces (2 levels)
                lines = stmt_code.split('\n')
                indented_lines = ['        ' + line for line in lines]  # 8 spaces for try block
                code.extend(indented_lines)
        
        code.extend([
            "        screen.update()",  # Update the screen after drawing
            "        screen.exitonclick()",  # Close window when clicked
            "    except turtle.Terminator:",
            "        pass",  # Handle window close gracefully
            "    finally:",
            "        try:",
            "            screen.mainloop()",  # Keep window open until user closes it
            "        except:",
            "            pass",  # Ignore any cleanup errors",
            "",
            "if __name__ == '__main__':",
            "    main()"
        ])
        return "\n".join(code)
    
    def generate_block(self, node: Block) -> str:
        code = []
        for statement in node.statements:
            stmt_code = self.generate(statement)
            if stmt_code:
                code.append(stmt_code)
        return "\n".join(code)
    
    def generate_variable_declaration(self, node: VariableDeclaration) -> str:
        value = self.generate_expression(node.value)
        return f"{node.name} = {value}"
    
    def generate_assignment(self, node: Assignment) -> str:
        value = self.generate_expression(node.value)
        return f"{node.name} = {value}"
    
    def generate_binary_operation(self, node: BinaryOperation) -> str:
        left = self.generate_expression(node.left)
        right = self.generate_expression(node.right)
        
        # Map Mesel operators to Python operators
        operator_map = {
            TokenType.PLUS: "+",
            TokenType.MINUS: "-",
            TokenType.TIMES: "*",
            TokenType.DIVIDE_OP: "/",
            TokenType.MODULO_OP: "%",
            TokenType.POWER_OP: "**",
            TokenType.EQUALS: "==",
            TokenType.NOT_EQUALS: "!=",
            TokenType.GREATER: ">",
            TokenType.LESS: "<",
            TokenType.GREATER_EQUALS: ">=",
            TokenType.LESS_EQUALS: "<="
        }
        
        operator = operator_map.get(node.operator, node.operator)
        return f"{left} {operator} {right}"
    
    def generate_unary_operation(self, node: UnaryOperation) -> str:
        expr = self.generate_expression(node.operand)
        operator = "-" if node.operator == TokenType.MINUS else "not "
        return f"{operator}{expr}"
    
    def generate_number(self, node: Number) -> str:
        return str(node.value)
    
    def generate_string(self, node: String) -> str:
        return f'"{node.value}"'
    
    def generate_identifier(self, node: Identifier) -> str:
        return node.name
    
    def generate_print(self, node: Print) -> str:
        return f"print({self.generate(node.expression)})"
    
    def generate_for_loop(self, node: ForLoop) -> str:
        code = []
        if node.variable is None:
            # Numeric range loop
            start = int(float(self.generate(node.start)))
            end = int(float(self.generate(node.end)))
            code.append(f"for _ in range({start}, {end}):")
        else:
            # Variable-based loop
            start = int(float(self.generate(node.start)))
            end = int(float(self.generate(node.end)))
            code.append(f"for {node.variable} in range({start}, {end}):")
        
        # Generate body with proper indentation
        body_code = self.generate(node.body)
        if body_code:
            # Split body code into lines and indent each line
            body_lines = body_code.split('\n')
            indented_body = '\n'.join("    " + line for line in body_lines)
            code.append(indented_body)
        
        return "\n".join(code)
    
    def generate_while_loop(self, node: WhileLoop) -> str:
        code = []
        code.append(f"while {self.generate(node.condition)}:")
        self.indent_level += 1
        for stmt in node.body:
            code.append(self.indent(self.generate(stmt)))
        self.indent_level -= 1
        return "\n".join(code)
    
    def generate_if_statement(self, node: IfStatement) -> str:
        code = []
        code.append(f"if {self.generate(node.condition)}:")
        self.indent_level += 1
        for stmt in node.then_branch:
            code.append(self.indent(self.generate(stmt)))
        self.indent_level -= 1
        
        if node.else_branch:
            code.append("else:")
            self.indent_level += 1
            for stmt in node.else_branch:
                code.append(self.indent(self.generate(stmt)))
            self.indent_level -= 1
        
        return "\n".join(code)
    
    def generate_break(self, node: Break) -> str:
        return "break"
    
    def generate_continue(self, node: Continue) -> str:
        return "continue"
    
    def generate_turtle_command(self, node: TurtleCommand) -> str:
        if node.command == TokenType.FORWARD:
            return f"t.forward({self.generate(node.argument)})"
        elif node.command == TokenType.TURN:
            return f"t.right({self.generate(node.argument)})"
        elif node.command == TokenType.PEN_DOWN:
            return "t.pendown()"
        elif node.command == TokenType.PEN_UP:
            return "t.penup()"
        else:
            raise Exception(f"Unknown turtle command: {node.command}")
    
    def generate_color_command(self, node: ColorCommand) -> str:
        color_map = {
            TokenType.RED: "red",
            TokenType.GREEN: "green",
            TokenType.BLUE: "blue",
            TokenType.YELLOW: "yellow",
            TokenType.BLACK: "black",
            TokenType.WHITE: "white"
        }
        return f"t.color('{color_map[node.color]}')"
    
    def generate_width_command(self, node: WidthCommand) -> str:
        return f"t.width({self.generate(node.width)})"
    
    def generate_expression(self, node: Expression) -> str:
        if isinstance(node, BinaryOperation):
            return self.generate_binary_operation(node)
        elif isinstance(node, UnaryOperation):
            return self.generate_unary_operation(node)
        elif isinstance(node, Identifier):
            return self.generate_identifier(node)
        elif isinstance(node, Number):
            return self.generate_number(node)
        elif isinstance(node, String):
            return self.generate_string(node)
        else:
            raise ValueError(f"Unknown expression type: {type(node)}")
    
    def visit(self, node: Node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: Node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit_block(self, node: Block):
        for statement in node.statements:
            self.visit(statement)
    
    def visit_assignment(self, node: Assignment):
        self.code.append('    ' * self.indent_level)
        self.code.append(f"{node.name} = ")
        self.visit(node.value)
        self.code.append('\n')
    
    def visit_number(self, node: Number):
        self.code.append(str(node.value))
    
    def visit_string(self, node: String):
        self.code.append(f'"{node.value}"')
    
    def visit_boolean(self, node: Boolean):
        self.code.append(str(node.value))
    
    def visit_identifier(self, node: Identifier):
        self.code.append(node.name)
    
    def visit_binary_op(self, node: BinaryOp):
        self.visit(node.left)
        self.code.append(f' {node.operator} ')
        self.visit(node.right)
    
    def visit_input(self, node: Input):
        if node.prompt:
            self.code.append('input(')
            self.visit(node.prompt)
            self.code.append(')')
        else:
            self.code.append('input()')
    
    def visit_input_statement(self, node: InputStatement):
        self.code.append('    ' * self.indent_level)
        self.code.append(f"{node.variable} = ")
        if node.prompt:
            self.code.append('input(')
            self.visit(node.prompt)
            self.code.append(')')
        else:
            self.code.append('input()')
        self.code.append('\n')
    
    def visit_if_statement(self, node: IfStatement):
        self.code.append('    ' * self.indent_level)
        self.code.append('if ')
        self.visit(node.condition)
        self.code.append(':\n')
        self.indent_level += 1
        self.visit(node.then_block)
        self.indent_level -= 1
        
        if node.else_block:
            self.code.append('    ' * self.indent_level)
            self.code.append('else:\n')
            self.indent_level += 1
            self.visit(node.else_block)
            self.indent_level -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        self.code.append('    ' * self.indent_level)
        self.code.append('while ')
        self.visit(node.condition)
        self.code.append(':\n')
        self.indent_level += 1
        self.visit(node.body)
        self.indent_level -= 1
    
    def visit_for_statement(self, node: ForStatement):
        self.code.append('    ' * self.indent_level)
        self.code.append('for _ in range(')
        self.visit(node.count)
        self.code.append('):\n')
        self.indent_level += 1
        self.visit(node.body)
        self.indent_level -= 1
    
    def visit_print_statement(self, node: PrintStatement):
        self.code.append('    ' * self.indent_level)
        self.code.append('print(')
        self.visit(node.expression)
        self.code.append(')\n')
    
    def visit_forward(self, node: Forward):
        self.code.append('    ' * self.indent_level)
        self.code.append('t.forward(')
        self.visit(node.distance)
        self.code.append(')\n')
    
    def visit_turn(self, node: Turn):
        self.code.append('    ' * self.indent_level)
        self.code.append('t.left(')
        self.visit(node.angle)
        self.code.append(')\n')
    
    def visit_pen_down(self, node: PenDown):
        self.code.append('    ' * self.indent_level)
        self.code.append('t.pendown()\n')
    
    def visit_pen_up(self, node: PenUp):
        self.code.append('    ' * self.indent_level)
        self.code.append('t.penup()\n')
    
    def indent(self, text: str) -> str:
        return "    " * self.indent_level + text 