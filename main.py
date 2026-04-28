import sys
from elli_runtime.lexer import Lexer
from elli_runtime.statement_parser import StatementParser
from elli_runtime.interpreter import Interpreter, ProgramTerminate
from elli_runtime.ast_nodes import ImportNode, FromImportNode
from elli_runtime.tokens import TokenType
from elli_runtime.errors import ELLIIndentationError, ELLIError
from colors import Colors
from elli_runtime.language_el import EL_KEYWORDS
from elli_runtime.language_en import EN_KEYWORDS

def validate_indentation(tokens):

    block_openers = {
        TokenType.IF,
        TokenType.FOR,
        TokenType.WHILE,
    }

    block_closers = {
        TokenType.END_IF,
        TokenType.END_FOR,
        TokenType.END_WHILE,
        TokenType.END_FUNCTION,
    }

    stack = []

    for i, token in enumerate(tokens):

        # Εξετάζουμε μόνο πρώτο token γραμμής
        if i > 0 and tokens[i - 1].type != TokenType.NEWLINE:
            continue

        if token.type == TokenType.NEWLINE:
            continue

        # FUNCTION OPENER (DECLARE ... AS FUNCTION)
        if (
            token.type == TokenType.DECLARE
            and i + 3 < len(tokens)
            and tokens[i + 2].type == TokenType.AS
            and tokens[i + 3].type == TokenType.FUNCTION
        ):
            stack.append(token.indent)
            continue

        # IF / FOR / WHILE
        if token.type in (TokenType.IF, TokenType.FOR, TokenType.WHILE):
            stack.append(token.indent)
            continue

        # ---- BLOCK CLOSER ----
        if token.type in block_closers:

            if not stack:
                raise ELLIIndentationError(
                    "ΣΦΑΛΜΑ_ΕΣΟΧΗΣ",
                    token.line,
                    "Απρόσμενο ΤΕΛΟΣ_..."
                )

            expected_indent = stack.pop()

            if token.indent != expected_indent:
                raise ELLIIndentationError(
                    "ΣΦΑΛΜΑ_ΕΣΟΧΗΣ",
                    token.line,
                    "Το ΤΕΛΟΣ_... δεν είναι σωστά ευθυγραμμισμένο"
                )

            continue

        # ---- INNER LINE ----
        if stack:
            if token.indent <= stack[-1]:
                raise ELLIIndentationError(
                    "ΣΦΑΛΜΑ_ΕΣΟΧΗΣ",
                    token.line,
                    "Αναμενόταν μεγαλύτερη εσοχή μετά από εντολή μπλοκ"
                )

    if stack:
        raise ELLIIndentationError(
            "ΣΦΑΛΜΑ_ΕΣΟΧΗΣ",
            tokens[-1].line,
            "Δεν έκλεισε σωστά ένα μπλοκ"
        )

def load_module(name, edition, registry):
    if name in registry:
        return
    filename = f"{name}.elli"

    try:
        with open(filename, "r", encoding="utf8") as f:
            code = f.read()
    except:
        from elli_runtime.errors import ELLINameError
        raise ELLINameError(0, name)
    from elli_runtime.errors import set_edition
    set_edition(edition)

    # Νέος interpreter για module
    module_interp = Interpreter()

    # Lex + Parse
    if edition == "EL":
        keyword_map = EL_KEYWORDS
        forbidden_map = EN_KEYWORDS
    else:
        keyword_map = EN_KEYWORDS
        forbidden_map = EL_KEYWORDS

    lexer = Lexer(code, keyword_map, forbidden_map)
    tokens = lexer.tokenize()
    validate_indentation(tokens)

    pos = 0
    while pos < len(tokens) and tokens[pos].type != TokenType.EOF:

        parser = StatementParser(tokens[pos:])
        ast = parser.parse()

        if ast is None:
            break

        module_interp.visit(ast)
        pos += parser.pos

    # Αποθήκευση public namespace
    registry[name] = {
        "variables": module_interp.scopes[0],
        "functions": module_interp.functions
    }

def run(code, edition):
    from elli_runtime.errors import set_edition
    set_edition(edition)
    try:
        # 🔹 Επιλογή Γλωσσικής Έκδοσης (CORE 1.0)
        if edition == "EL":
            keyword_map = EL_KEYWORDS
            forbidden_map = EN_KEYWORDS
        elif edition == "EN":
            keyword_map = EN_KEYWORDS
            forbidden_map = EL_KEYWORDS
        else:
            raise Exception("Άγνωστη γλωσσική έκδοση")

        lexer = Lexer(code, keyword_map, forbidden_map)
        tokens = lexer.tokenize()
        validate_indentation(tokens)
        # ---- MODULE PRE-LOAD ----
        module_registry = {}
        pos_scan = 0

        while pos_scan < len(tokens) and tokens[pos_scan].type != TokenType.EOF:

            parser = StatementParser(tokens[pos_scan:])
            ast = parser.parse()

            if isinstance(ast, ImportNode):
                load_module(ast.module_name, edition, module_registry)

            if isinstance(ast, FromImportNode):
                load_module(ast.module_name, edition, module_registry)

                module_name = ast.module_name
                element_name = ast.element_name

                module_data = module_registry[module_name]

                # Variable import
                if element_name in module_data["variables"]:
                    module_registry.setdefault("__selective__", {})
                    module_registry["__selective__"][element_name] = (
                        "var",
                        module_data["variables"][element_name]
                    )

                # Function import
                elif element_name in module_data["functions"]:
                    module_registry.setdefault("__selective__", {})
                    module_registry["__selective__"][element_name] = (
                        "func",
                        module_data["functions"][element_name]
                    )

                else:
                    from elli_runtime.errors import ELLINameError
                    raise ELLINameError(0, element_name)

            if parser.pos == 0:
                break

            pos_scan += parser.pos

        interp = Interpreter()
        interp.modules = module_registry

        # APPLY SELECTIVE IMPORTS
        if "__selective__" in module_registry:

            for name, (kind, value) in module_registry["__selective__"].items():

                if kind == "var":
                    interp.scopes[0][name] = value

                elif kind == "func":
                    interp.functions[name] = value

        pos = 0

        while pos < len(tokens) and tokens[pos].type != TokenType.EOF:

            parser = StatementParser(tokens[pos:])
            ast = parser.parse()

            if ast is None:
                break

            # Αγνόηση Import nodes (ήδη φορτώθηκαν στο pre-load)
            # ---- IMPORT HANDLING ----
            if isinstance(ast, ImportNode):
                pos += parser.pos
                continue

            if isinstance(ast, FromImportNode):
                pos += parser.pos
                continue
            
            if parser.pos == 0:
                raise Exception("Parser stuck")

            interp.visit(ast)

            pos += parser.pos

    except ProgramTerminate:
        return

    except ELLIError as e:
        print(Colors.RED + str(e) + Colors.RESET)
        return

    except Exception as e:
        if edition == "EN":
            print("INTERNAL ERROR:", e)
        else:
            print("ΕΣΩΤΕΡΙΚΟ ΣΦΑΛΜΑ:", e)
        return


def run_file(path, edition):
    with open(path, "r", encoding="utf8") as f:
        code = f.read()

    run(code, edition)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Χρήση:")
        print("python main.py test.elli EL")
        print("python main.py test.elli EN")
        sys.exit(1)

    file = sys.argv[1]
    edition = sys.argv[2].upper()

    run_file(file, edition)