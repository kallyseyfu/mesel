# መሰል (Mesel) Programming Language

መሰል (Mesel) is an educational programming language designed to teach programming and mathematics concepts to Amharic-speaking children (ages 8-16). The language uses Amharic keywords and translates to Python, making it accessible while maintaining powerful programming capabilities.

## Features

- Amharic keywords for basic programming concepts
- Built-in turtle graphics for visual learning
- Simple math operations
- Basic control structures
- Python-compatible output

## Language Keywords

### Control Structures
- `ጀምር` (jemr) - begin/start
- `ጨርስ` (chers) - end
- `እድግ` (idg) - for
- `ከሆነ` (kehone) - if
- `ካልሆነ` (kalhone) - else
- `ድገም` (dgem) - while

### Data Types
- `ቁጥር` (kutr) - number
- `ፊደል` (fidel) - string
- `እውነት` (iwnet) - boolean

### Turtle Graphics
- `ሂድ` (hid) - forward
- `ዙር` (zur) - turn
- `ስዕል_ጀምር` (sil_jemr) - pendown
- `ስዕል_አቁም` (sil_akum) - penup

### Variables and Operations
- `አስቀምጥ` (askemT) - assign/let
- `ያሳይ` (yasay) - print
- `ደምር` (demr) - add
- `ቀንስ` (kens) - subtract
- `አባዛ` (abaza) - multiply
- `ክፈል` (kifel) - divide

## Example Programs

### 1. Drawing a Square
```
ጀምር
    ስዕል_ጀምር
    እድግ 4
        ሂድ 100
        ዙር 90
    ጨርስ
ጨርስ
```

### 2. Basic Math Operations
```
ጀምር
    አስቀምጥ ሀ = 10
    አስቀምጥ ለ = 5
    አስቀምጥ ውጤት = ደምር ሀ ለ
    ያሳይ ውጤት
ጨርስ
```

### 3. Conditional Statement
```
ጀምር
    አስቀምጥ እድሜ = 15
    ከሆነ እድሜ > 13
        ያሳይ "ታላቅ ልጅ ነህ"
    ካልሆነ
        ያሳይ "ታናሽ ልጅ ነህ"
    ጨርስ
ጨርስ
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mesel.git
cd mesel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Write your Mesel code in a `.mesel` file
2. Run the translator:
```bash
python translator.py your_program.mesel
```

## Development Status

Current implementation includes:
- [x] Lexer (Tokenizer)
- [ ] Parser
- [ ] Python Code Generator
- [ ] Standard Library
- [ ] Documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.