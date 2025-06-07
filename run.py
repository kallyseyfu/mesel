import sys
import os
import subprocess
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def run_mesel_file(filename: str):
    try:
        # Read the Mesel source code
        with open(filename, 'r', encoding='utf-8') as file:
            source = file.read()
        
        # Lexical analysis
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Code generation
        generator = CodeGenerator()
        python_code = generator.generate(ast)
        
        # Write the generated Python code to a temporary file
        temp_file = filename.replace('.mesel', '.py')
        with open(temp_file, 'w', encoding='utf-8') as file:
            file.write(python_code)
        
        # Execute the generated Python code using the current Python interpreter
        python_exe = sys.executable
        subprocess.run([python_exe, temp_file], check=True)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run.py <mesel_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not filename.endswith('.mesel'):
        print("Error: File must have .mesel extension")
        sys.exit(1)
    
    run_mesel_file(filename) 