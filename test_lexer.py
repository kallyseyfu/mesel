import unittest
from lexer import Lexer, TokenType, Token

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        text = """
        ጀምር
        አስቀምጥ ሀ = 5
        ከሆነ ሀ = 5 ድገም
        ሂድ 100
        ዙር 90
        ጨርስ
        """
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        
        # Remove newlines and EOF for easier testing
        tokens = [token for token in tokens if token.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        expected = [
            Token(TokenType.BEGIN, 'ጀምር', 2, 9),
            Token(TokenType.ASSIGN, 'አስቀምጥ', 3, 9),
            Token(TokenType.IDENTIFIER, 'ሀ', 3, 13),
            Token(TokenType.EQUALS, '=', 3, 15),
            Token(TokenType.NUMBER, '5', 3, 17),
            Token(TokenType.IF, 'ከሆነ', 4, 9),
            Token(TokenType.IDENTIFIER, 'ሀ', 4, 13),
            Token(TokenType.EQUALS, '=', 4, 15),
            Token(TokenType.NUMBER, '5', 4, 17),
            Token(TokenType.WHILE, 'ድገም', 4, 19),
            Token(TokenType.FORWARD, 'ሂድ', 5, 9),
            Token(TokenType.NUMBER, '100', 5, 13),
            Token(TokenType.TURN, 'ዙር', 6, 9),
            Token(TokenType.NUMBER, '90', 6, 13),
            Token(TokenType.END, 'ጨርስ', 7, 9),
        ]
        
        self.assertEqual(len(tokens), len(expected))
        for actual, expected in zip(tokens, expected):
            self.assertEqual(actual.type, expected.type)
            self.assertEqual(actual.value, expected.value)
    
    def test_arithmetic_operations(self):
        text = """
        አስቀምጥ ውጤት = 10 + 5 - 3 * 2 / 1
        """
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        
        # Remove newlines and EOF for easier testing
        tokens = [token for token in tokens if token.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        expected_types = [
            TokenType.ASSIGN,
            TokenType.IDENTIFIER,
            TokenType.EQUALS,
            TokenType.NUMBER,
            TokenType.PLUS,
            TokenType.NUMBER,
            TokenType.MINUS,
            TokenType.NUMBER,
            TokenType.TIMES,
            TokenType.NUMBER,
            TokenType.DIVIDE_OP,
            TokenType.NUMBER,
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for token, expected_type in zip(tokens, expected_types):
            self.assertEqual(token.type, expected_type)

if __name__ == '__main__':
    unittest.main() 