from enum import Enum
import re
from typing import List, NamedTuple

class TokenType(Enum):
    # Keywords
    BEGIN = 'ጀምር'        # jemr
    END = 'ጨርስ'         # chers
    FOR = 'እድግ'         # idg
    IF = 'ከሆነ'         # kehone
    ELSE = 'ካልሆነ'      # kalhone
    WHILE = 'ድገም'      # dgem
    BREAK = 'ተው'        # tew
    CONTINUE = 'ቀጥል'    # ketl
    
    # Data Types
    NUMBER_TYPE = 'ቁጥር'  # kutr
    STRING_TYPE = 'ፊደል'  # fidel
    BOOL_TYPE = 'እውነት'   # iwnet
    
    # Turtle Commands
    FORWARD = 'ሂድ'      # hid
    TURN = 'ዙር'         # zur
    PEN_DOWN = 'ስዕል_ጀምር' # sil_jemr
    PEN_UP = 'ስዕል_አቁም'   # sil_akum
    COLOR = 'ቀለም'      # kelem
    WIDTH = 'ስፋት'      # sfet
    
    # Colors
    RED = 'ቀይ'         # key
    GREEN = 'አረንጓዴ'   # arenguade
    BLUE = 'ሰማያዊ'     # semayawi
    YELLOW = 'ቢጫ'       # bicha
    BLACK = 'ጥቁር'      # tkur
    WHITE = 'ነጭ'        # nech
    
    # Variables and Operations
    ASSIGN = 'አስቀምጥ'    # askemT
    PRINT = 'ያሳይ'       # yasay
    ADD = 'ደምር'        # demr
    SUBTRACT = 'ቀንስ'    # kens
    MULTIPLY = 'አባዛ'    # abaza
    DIVIDE = 'ክፈል'      # kifel
    MODULO = 'ቀሪ'       # keri
    POWER = 'ደረጃ'      # dereja
    INCREMENT = 'ጨምር'    # chemr
    DECREMENT = 'ቀንስ'    # kens
    
    # Comparison Operators
    EQUALS = '=='        # equals
    NOT_EQUALS = '!='    # not equals
    GREATER = '>'        # greater than
    LESS = '<'           # less than
    GREATER_EQUALS = '>=' # greater or equal
    LESS_EQUALS = '<='   # less or equal
    
    # Logical Operators
    AND = 'እና'         # ena
    OR = 'ወይም'        # weyim
    NOT = 'አይደለም'     # aydel
    
    # Symbols
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'
    ASSIGN_OP = '='
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE_OP = '/'
    MODULO_OP = '%'
    POWER_OP = '**'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    COMMA = ','
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'

class Token(NamedTuple):
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.line = 1
        self.column = 1
        
        # Create keywords dictionary
        self.keywords = {
            'ጀምር': TokenType.BEGIN,
            'ጨርስ': TokenType.END,
            'እድግ': TokenType.FOR,
            'ከሆነ': TokenType.IF,
            'ካልሆነ': TokenType.ELSE,
            'ድገም': TokenType.WHILE,
            'ተው': TokenType.BREAK,
            'ቀጥል': TokenType.CONTINUE,
            'ቁጥር': TokenType.NUMBER_TYPE,
            'ፊደል': TokenType.STRING_TYPE,
            'እውነት': TokenType.BOOL_TYPE,
            'ሂድ': TokenType.FORWARD,
            'ዙር': TokenType.TURN,
            'ስዕል_ጀምር': TokenType.PEN_DOWN,
            'ስዕል_አቁም': TokenType.PEN_UP,
            'ቀለም': TokenType.COLOR,
            'ስፋት': TokenType.WIDTH,
            'ቀይ': TokenType.RED,
            'አረንጓዴ': TokenType.GREEN,
            'ሰማያዊ': TokenType.BLUE,
            'ቢጫ': TokenType.YELLOW,
            'ጥቁር': TokenType.BLACK,
            'ነጭ': TokenType.WHITE,
            'አስቀምጥ': TokenType.ASSIGN,
            'ያሳይ': TokenType.PRINT,
            'ደምር': TokenType.ADD,
            'ቀንስ': TokenType.SUBTRACT,
            'አባዛ': TokenType.MULTIPLY,
            'ክፈል': TokenType.DIVIDE,
            'ቀሪ': TokenType.MODULO,
            'ደረጃ': TokenType.POWER,
            'ጨምር': TokenType.INCREMENT,
            'ቀንስ': TokenType.DECREMENT,
            'እና': TokenType.AND,
            'ወይም': TokenType.OR,
            'አይደለም': TokenType.NOT
        }
    
    def error(self):
        raise Exception(f'Invalid character {self.current_char} at line {self.line}, column {self.column}')
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
    
    def number(self) -> Token:
        result = ''
        token_column = self.column
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
            
        return Token(TokenType.NUMBER, result, self.line, token_column)
    
    def string(self) -> Token:
        result = ''
        token_column = self.column
        self.advance()  # Skip opening quote
        
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        if self.current_char == '"':
            self.advance()  # Skip closing quote
        else:
            raise Exception(f'Unterminated string at line {self.line}, column {token_column}')
        
        return Token(TokenType.STRING, result, self.line, token_column)
    
    def identifier(self) -> Token:
        result = ''
        token_column = self.column
        
        while self.current_char and (self.is_amharic(self.current_char) or 
                                   self.current_char.isalnum() or 
                                   self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, token_column)
    
    @staticmethod
    def is_amharic(char: str) -> bool:
        return '\u1200' <= char <= '\u137F'
    
    def get_next_token(self) -> Token:
        while self.current_char:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                token = self.number()
                print(f"Found number token: {token}")
                return token
            
            # Strings
            if self.current_char == '"':
                token = self.string()
                print(f"Found string token: {token}")
                return token
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.is_amharic(self.current_char):
                token = self.identifier()
                print(f"Found identifier token: {token}")
                return token
            
            # Two-character operators
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(TokenType.EQUALS, '==', self.line, self.column - 2)
                print(f"Found equals token: {token}")
                return token
            
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(TokenType.NOT_EQUALS, '!=', self.line, self.column - 2)
                print(f"Found not equals token: {token}")
                return token
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(TokenType.GREATER_EQUALS, '>=', self.line, self.column - 2)
                print(f"Found greater equals token: {token}")
                return token
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                token = Token(TokenType.LESS_EQUALS, '<=', self.line, self.column - 2)
                print(f"Found less equals token: {token}")
                return token
            
            # Single-character operators
            if self.current_char == '=':
                self.advance()
                token = Token(TokenType.ASSIGN_OP, '=', self.line, self.column - 1)
                print(f"Found assign token: {token}")
                return token
            
            if self.current_char == '+':
                self.advance()
                token = Token(TokenType.PLUS, '+', self.line, self.column - 1)
                print(f"Found plus token: {token}")
                return token
            
            if self.current_char == '-':
                self.advance()
                token = Token(TokenType.MINUS, '-', self.line, self.column - 1)
                print(f"Found minus token: {token}")
                return token
            
            if self.current_char == '*':
                if self.peek() == '*':
                    self.advance()
                    self.advance()
                    token = Token(TokenType.POWER_OP, '**', self.line, self.column - 2)
                    print(f"Found power token: {token}")
                    return token
                self.advance()
                token = Token(TokenType.TIMES, '*', self.line, self.column - 1)
                print(f"Found times token: {token}")
                return token
            
            if self.current_char == '/':
                self.advance()
                token = Token(TokenType.DIVIDE_OP, '/', self.line, self.column - 1)
                print(f"Found divide token: {token}")
                return token
            
            if self.current_char == '%':
                self.advance()
                token = Token(TokenType.MODULO_OP, '%', self.line, self.column - 1)
                print(f"Found modulo token: {token}")
                return token
            
            if self.current_char == '(':
                self.advance()
                token = Token(TokenType.LPAREN, '(', self.line, self.column - 1)
                print(f"Found lparen token: {token}")
                return token
            
            if self.current_char == ')':
                self.advance()
                token = Token(TokenType.RPAREN, ')', self.line, self.column - 1)
                print(f"Found rparen token: {token}")
                return token
            
            if self.current_char == '{':
                self.advance()
                token = Token(TokenType.LBRACE, '{', self.line, self.column - 1)
                print(f"Found lbrace token: {token}")
                return token
            
            if self.current_char == '}':
                self.advance()
                token = Token(TokenType.RBRACE, '}', self.line, self.column - 1)
                print(f"Found rbrace token: {token}")
                return token
            
            if self.current_char == ',':
                self.advance()
                token = Token(TokenType.COMMA, ',', self.line, self.column - 1)
                print(f"Found comma token: {token}")
                return token
            
            if self.current_char == '>':
                self.advance()
                token = Token(TokenType.GREATER, '>', self.line, self.column - 1)
                print(f"Found greater token: {token}")
                return token
            
            if self.current_char == '<':
                self.advance()
                token = Token(TokenType.LESS, '<', self.line, self.column - 1)
                print(f"Found less token: {token}")
                return token
            
            if self.current_char == '\n':
                self.advance()
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column - 1)
                print(f"Found newline token: {token}")
                return token
            
            print(f"Invalid character: {self.current_char} at line {self.line}, column {self.column}")
            self.error()
        
        return Token(TokenType.EOF, '', self.line, self.column)
    
    def peek(self) -> str:
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def tokenize(self) -> List[Token]:
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

# Example usage
if __name__ == "__main__":
    # Test the lexer
    test_code = '''
    ጀምር
        አስቀምጥ ሀ = 10
        አስቀምጥ ለ = 5
        አስቀምጥ ድምር = ሀ ደምር ለ
        ያሳይ "ድምር: " ድምር
    ጨርስ
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    # Print tokens for debugging
    for token in tokens:
        print(f"Token: {token.type} = {token.value}")
