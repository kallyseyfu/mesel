import unittest
from lexer import Lexer
from parser import Parser
from ast_nodes import *

class TestParser(unittest.TestCase):
    def parse_code(self, code: str) -> Program:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_basic_program(self):
        code = """
        ጀምር
            አስቀምጥ ሀ = 5
            ያሳይ ሀ
        ጨርስ
        """
        ast = self.parse_code(code)
        
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 2)
        
        # Test assignment
        assign = ast.statements[0]
        self.assertIsInstance(assign, Assignment)
        self.assertEqual(assign.name, 'ሀ')
        self.assertIsInstance(assign.value, Number)
        self.assertEqual(assign.value.value, 5.0)
        
        # Test print
        print_stmt = ast.statements[1]
        self.assertIsInstance(print_stmt, PrintStatement)
        self.assertIsInstance(print_stmt.expression, Identifier)
        self.assertEqual(print_stmt.expression.name, 'ሀ')
    
    def test_turtle_graphics(self):
        code = """
        ጀምር
            ስዕል_ጀምር
            ሂድ 100
            ዙር 90
            ስዕል_አቁም
        ጨርስ
        """
        ast = self.parse_code(code)
        
        self.assertEqual(len(ast.statements), 4)
        self.assertIsInstance(ast.statements[0], PenDown)
        
        forward = ast.statements[1]
        self.assertIsInstance(forward, Forward)
        self.assertIsInstance(forward.distance, Number)
        self.assertEqual(forward.distance.value, 100.0)
        
        turn = ast.statements[2]
        self.assertIsInstance(turn, Turn)
        self.assertIsInstance(turn.angle, Number)
        self.assertEqual(turn.angle.value, 90.0)
        
        self.assertIsInstance(ast.statements[3], PenUp)
    
    def test_if_statement(self):
        code = """
        ጀምር
            አስቀምጥ እድሜ = 15
            ከሆነ እድሜ > 13
                ያሳይ "ታላቅ ልጅ ነህ"
            ጨርስ
        ጨርስ
        """
        ast = self.parse_code(code)
        
        self.assertEqual(len(ast.statements), 2)
        
        if_stmt = ast.statements[1]
        self.assertIsInstance(if_stmt, IfStatement)
        self.assertIsInstance(if_stmt.condition, BinaryOp)
        self.assertIsInstance(if_stmt.then_block, Block)
        self.assertEqual(len(if_stmt.then_block.statements), 1)
    
    def test_arithmetic(self):
        code = """
        ጀምር
            አስቀምጥ ውጤት = 10 + 5 * 2
        ጨርስ
        """
        ast = self.parse_code(code)
        
        assign = ast.statements[0]
        self.assertIsInstance(assign.value, BinaryOp)
        self.assertEqual(assign.value.operator, '+')
        self.assertIsInstance(assign.value.right, BinaryOp)
        self.assertEqual(assign.value.right.operator, '*')

if __name__ == '__main__':
    unittest.main() 