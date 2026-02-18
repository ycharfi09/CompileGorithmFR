# FEATURES.md - Complete Feature List

## CompileGorithmFR Feature Reference

### Supported Data Types

1. **Entier** - Integer numbers
   - Example: `x: Entier`
   - Default value: 0

2. **Reel / Réel** - Floating-point numbers
   - Example: `prix: Reel`
   - Default value: 0.0

3. **Caractere / Caractère** - Single character
   - Example: `lettre: Caractere`
   - Default value: ''

4. **Chaine / Chaîne** - String
   - Example: `message: Chaine`
   - Default value: ''

5. **Booleen / Booléen** - Boolean
   - Example: `estVrai: Booleen`
   - Values: `Vrai`, `Faux`
   - Default value: Faux (False)

6. **Tableau** - Array
   - Example: `notes: Tableau[10] de Entier`
   - Zero-indexed
   - Fixed size

### Control Structures

#### If-Then-Else (Si-Alors-Sinon)
```
Si condition Alors
    // statements when true
Sinon
    // statements when false (optional)
FinSi
```

#### For Loop (Pour)
```
Pour variable allant de debut a fin Faire
    // loop body
FinPour
```
- Inclusive range (includes both start and end)
- Accepts both 'a' and 'à'

#### While Loop (TantQue)
```
TantQue condition Faire
    // loop body
FinTantQue
```

#### Repeat-Until Loop (Repeter-Jusqu'a)
```
Repeter
    // loop body
Jusqu'a condition
```
- Executes at least once
- Continues until condition becomes true
- Accepts both "Jusqu'a" and "Jusqu'à"

### Operators

#### Arithmetic Operators
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (real division)
- `Div` Integer division
- `Mod` Modulo (remainder)

#### Comparison Operators
- `=` Equal to
- `<>` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal to
- `>=` Greater than or equal to

#### Logical Operators
- `ET` Logical AND
- `OU` Logical OR
- `NON` Logical NOT

#### Assignment
- `:=` Assignment operator

### Input/Output Operations

#### Write (Ecrire / Écrire)
```
Ecrire(expression1, expression2, ...)
```
- Prints expressions separated by spaces
- Can mix strings, numbers, and variables

#### Read (Lire)
```
Lire(variable1, variable2, ...)
```
- Reads values from standard input
- Automatically converts to appropriate type

### Program Structure

```
Algorithme NomAlgorithme
Variables
    var1: Type1
    var2, var3: Type2
    tableau: Tableau[size] de Type3
Debut
    // Program statements
Fin
```

### Comments

```
// Single line comment
```

### Operator Precedence (Highest to Lowest)

1. Parentheses `( )`
2. Unary operators: `-` (negation), `NON`
3. Multiplicative: `*`, `/`, `Div`, `Mod`
4. Additive: `+`, `-`
5. Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`
6. Logical AND: `ET`
7. Logical OR: `OU`

### Variable Naming Rules

- Start with a letter
- Can contain letters, numbers, and underscores
- Case-sensitive
- Can use French accented characters
- Cannot be a reserved keyword

### Reserved Keywords

- Algorithme, Debut, Fin
- Variables
- Si, Alors, Sinon, FinSi
- Pour, allant, Faire, FinPour
- TantQue, FinTantQue
- Repeter/Répéter, Jusqu'a/Jusqu'à
- Ecrire/Écrire, Lire
- Entier, Reel/Réel, Caractere/Caractère, Chaine/Chaîne, Booleen/Booléen
- Tableau
- Vrai, Faux
- ET, OU, NON
- Mod, Div

### Array Indexing

- Arrays are zero-indexed (first element is at index 0)
- Size is specified at declaration: `Tableau[n]`
- Access: `array[index]`
- Assignment: `array[index] := value`
- Out-of-bounds access raises a runtime error

### Error Handling

The interpreter provides clear error messages for:
- Syntax errors (during parsing)
- Runtime errors (during execution)
  - Division by zero
  - Array index out of bounds
  - Undeclared variables
  - Type mismatches

### Command Line Usage

```bash
# Run an algorithm file
python3 compilegorithm.py file.algo

# Run with debug output
python3 compilegorithm.py file.algo --debug

# Show example algorithm
python3 compilegorithm.py --example

# Show help
python3 compilegorithm.py --help
```

### Supported File Extension

- `.algo` - Algorithm source files

### Examples Provided

1. `bonjour.algo` - Basic I/O
2. `somme.algo` - Simple arithmetic
3. `factorielle.algo` - For loop with factorial
4. `tableau.algo` - Array operations
5. `conditions.algo` - If-else statements
6. `boucle_tantque.algo` - While loop
7. `boucle_repeter.algo` - Repeat-until loop
8. `recherche_tableau.algo` - Array search with boolean logic
9. `pgcd.algo` - GCD algorithm with modulo
10. `demo_complet.algo` - Comprehensive demonstration

### Testing

Run the test suite:
```bash
python3 test_interpreter.py
```

All 11 tests cover:
- Lexer functionality (tokenization)
- Parser functionality (AST construction)
- Interpreter functionality (execution)
- Arithmetic operations
- Control structures (if, for, while)
- Arrays
- Boolean logic

### Implementation Details

- **Language**: Python 3.7+
- **Architecture**: Three-stage compilation
  1. Lexer (tokenization)
  2. Parser (AST construction)
  3. Interpreter (execution)
- **No external dependencies** - Uses only Python standard library
- **Platform**: Cross-platform (Windows, macOS, Linux)

### Limitations

- No function/procedure definitions
- No user-defined types/structures
- No file I/O operations
- No string manipulation functions
- Arrays must have fixed size known at declaration
- No multidimensional arrays
- No recursive structures

### Future Enhancements (Potential)

- Function/procedure support (Fonction, Procedure)
- String manipulation operations
- File I/O
- More data structures (structures, records)
- Multidimensional arrays
- Step parameter for For loops
- Break/Continue statements
- Switch/Case statements
