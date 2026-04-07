# ELLI Programming Language

ELLI is a strict, bilingual programming language with a stable CORE designed for educational clarity and long-term systems growth.

## What is ELLI

ELLI is a programming language built around:

- strict typing
- explicit syntax
- deterministic execution
- bilingual keyword editions (EL / EN)
- a stable CORE that grows through compatible extensions

Its current public core is defined through CORE 1.0, 1.1, 1.2, and 1.3. These documents define the language syntax, type system, infrastructure namespaces, structured data, constants, and module architecture. fileciteturn3file0 fileciteturn3file1 fileciteturn3file2 fileciteturn3file3

## What ELLI supports up to v1.0.0

Version 1.0.0 includes the stable CORE 1.x foundation:

- strict variable declarations with explicit types
- explicit block endings and indentation rules
- functions, conditions, loops, logical operators, and error handling
- lists and structured key-value data through `ΔΟΜΗ`
- `ΑΡΧΕΙΟ`, `JSON`, and `HTTP` namespaces
- constants with `ΣΤΑΘΕΡΑ`
- module system with namespace access and selective import
- EL and EN language editions with the same internal behavior and AST model fileciteturn3file0 fileciteturn3file1 fileciteturn3file2 fileciteturn3file3

## How to run a `.elli` file

Greek edition:

```bash
python main.py path/to/file.elli EL
```

English edition:

```bash
python main.py path/to/file.elli EN
```

Examples:

```bash
python main.py tests/test_el_1.elli EL
python main.py tests/test_en_1.elli EN
```

## EL / EN editions

ELLI supports two keyword editions:

- `EL` → Greek keywords
- `EN` → English keywords

Both editions:

- use the same runtime
- follow the same syntax rules
- use the same type system
- produce the same execution behavior

A single source file must belong to one edition only. Mixed EL/EN keywords in the same file are not allowed. fileciteturn3file0

## Where the docs are

Project documentation is in the `docs/` folder:

- `docs/elli_readme.md`
- `docs/elli_guide.md`
- `docs/elli_language_reference.md`

Core specification PDFs:

- `ELLI Core 1.0.pdf`
- `ELLI Core 1.1.pdf`
- `ELLI Core 1.2.pdf`
- `ELLI Core 1.3.pdf`

## Which tests to run first

Recommended first test order:

```bash
python main.py tests/full_language_test.elli EL
python main.py tests/full_core_test_en.elli EN
python main.py tests/test_el_1.elli EL
python main.py tests/test_el_2.elli EL
python main.py tests/test_en_1.elli EN
python main.py tests/test_en_2.elli EN
```

## Project structure

```text
D:\elli
│  main.py
│  math_el.elli
│  math_en.elli
│  README.md
│
├─ elli_runtime
│   │ __init__.py
│   │ ast_nodes.py
│   │ errors.py
│   │ expression_parser.py
│   │ interpreter.py
│   │ language_el.py
│   │ language_en.py
│   │ lexer.py
│   │ statement_parser.py
│   │ tokens.py
│
├─ docs
│   │ elli_guide.md
│   │ elli_language_reference.md
│   │ elli_readme.md
│
└─ tests
    │ full_language_test.elli
    │ full_core_test_en.elli
    │ test_el_1.elli
    │ test_el_2.elli
    │ test_en_1.elli
    │ test_en_2.elli
```

## Version 1.0.0 focus

ELLI v1.0.0 is the first stable public foundation of the language. The goal of this release is not to provide a huge ecosystem yet, but to provide a clean, strict, well-documented base that can grow without breaking its philosophy.

## 📬 Contact & Community

If you want to get in touch, ask questions, or follow the development of ELLI, you can use the following:

### 📧 Email
elli.language.dev@gmail.com

For:
- general questions
- feedback
- collaboration inquiries

---

### 💬 GitHub Discussions
Use Discussions for:
- ideas
- questions
- design conversations
- language proposals

---

### 🐛 GitHub Issues
Use Issues for:
- bug reports
- unexpected behavior
- runtime or parser problems

Please include:
- a minimal reproducible example
- the ELLI edition (EL / EN)
- expected vs actual behavior

## License

This project is licensed under the MIT License.