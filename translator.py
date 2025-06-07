import sys
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def translate_file(input_file: str, output_file: str = None):
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = input_file.rsplit('.', 1)[0] + '.py'
    
    try:
        # Tokenize
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Generate code
        generator = CodeGenerator()
        python_code = generator.generate(ast)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print(f"Successfully translated {input_file} to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python translator.py input_file [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    translate_file(input_file, output_file)

if __name__ == '__main__':
    main() 