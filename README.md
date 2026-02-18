# CompileGorithmFR

A way to actually run the algorithms you study at school in the Tunisian IT curriculum!

This project provides an interpreter for the French-based algorithmic language used in Tunisian schools (and other francophone countries), allowing you to write and execute algorithms using the same syntax you learn in class.

## Features

- ✅ Full support for Tunisian school algorithm syntax
- ✅ Variable declarations with types (Entier, Reel, Caractere, Chaine, Booleen)
- ✅ Arrays (Tableau)
- ✅ Control structures (Si/Alors/Sinon, Pour, TantQue, Repeter/Jusqu'a)
- ✅ Input/Output operations (Lire, Ecrire)
- ✅ Arithmetic and logical operators
- ✅ Command-line interface for running algorithm files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ycharfi09/CompileGorithmFR.git
cd CompileGorithmFR
```

2. Make sure you have Python 3.7+ installed:
```bash
python3 --version
```

3. Make the main script executable (optional):
```bash
chmod +x compilegorithm.py
```

## Usage

### Running an Algorithm File

```bash
python3 compilegorithm.py examples/somme.algo
```

### With Debug Output

```bash
python3 compilegorithm.py examples/factorielle.algo --debug
```

### Show Example Algorithm

```bash
python3 compilegorithm.py --example
```

## Language Syntax

### Basic Structure

```
Algorithme NomAlgorithme
Variables
    variable1: Type
    variable2, variable3: Type
Debut
    // Votre code ici
Fin
```

### Data Types

- `Entier` - Integer numbers
- `Reel` / `Réel` - Floating-point numbers  
- `Caractere` / `Caractère` - Single character
- `Chaine` / `Chaîne` - String
- `Booleen` / `Booléen` - Boolean (Vrai/Faux)
- `Tableau[n] de Type` - Array of n elements

### Assignment

```
variable := valeur
tableau[index] := valeur
```

### Input/Output

```
Ecrire("Message", variable)
Lire(variable)
```

### Conditional Statements

```
Si condition Alors
    // instructions
Sinon
    // instructions
FinSi
```

### Loops

**For Loop:**
```
Pour variable allant de debut a fin Faire
    // instructions
FinPour
```

**While Loop:**
```
TantQue condition Faire
    // instructions
FinTantQue
```

**Repeat Loop:**
```
Repeter
    // instructions
Jusqu'a condition
```

### Operators

**Arithmetic:** `+`, `-`, `*`, `/`, `Div` (integer division), `Mod` (modulo)

**Comparison:** `=`, `<>`, `<`, `>`, `<=`, `>=`

**Logical:** `ET` (AND), `OU` (OR), `NON` (NOT)

## Examples

### Simple Addition

```
Algorithme Somme
Variables
    a, b, resultat: Entier
Debut
    a := 15
    b := 27
    resultat := a + b
    Ecrire("La somme de", a, "et", b, "est", resultat)
Fin
```

### Factorial Calculation

```
Algorithme Factorielle
Variables
    n, i, fact: Entier
Debut
    n := 5
    fact := 1
    Pour i allant de 1 à n Faire
        fact := fact * i
    FinPour
    Ecrire("Factorielle de", n, "est", fact)
Fin
```

### Working with Arrays

```
Algorithme TableauSimple
Variables
    notes: Tableau[5] de Entier
    i, somme: Entier
    moyenne: Reel
Debut
    notes[0] := 15
    notes[1] := 18
    notes[2] := 12
    notes[3] := 16
    notes[4] := 14
    
    somme := 0
    Pour i allant de 0 à 4 Faire
        somme := somme + notes[i]
    FinPour
    
    moyenne := somme / 5
    Ecrire("Somme des notes:", somme)
    Ecrire("Moyenne:", moyenne)
Fin
```

More examples can be found in the `examples/` directory.

## File Extension

Algorithm files should use the `.algo` extension.

## Project Structure

```
CompileGorithmFR/
├── compilegorithm.py    # Main CLI interface
├── lexer.py             # Lexical analyzer (tokenizer)
├── parser.py            # Syntax analyzer (parser)
├── interpreter.py       # Code interpreter/executor
├── examples/            # Example algorithm files
│   ├── bonjour.algo
│   ├── somme.algo
│   ├── factorielle.algo
│   ├── tableau.algo
│   └── conditions.algo
└── README.md
```

## How It Works

1. **Lexer**: Converts source code into tokens
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
3. **Interpreter**: Executes the AST

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Add more examples

## License

MIT License - see LICENSE file for details.

## Author

Youssef Charfi

## Acknowledgments

This project aims to help students practice and understand algorithms by providing a way to execute the pseudocode they learn in class, making algorithmic concepts more concrete and easier to grasp.
