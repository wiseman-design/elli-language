# Interpreter που διαβάζει AST nodes
import json
from .errors import ELLIKeyError
from .ast_nodes import *
from .tokens import TokenType
from .errors import GreekLangRuntimeError
from .errors import (
    ELLINameError,
    ELLITypeError,
    ELLIZeroDivisionError,
    ELLIBlockError,
    ELLIError,
    ELLISyntaxError
)
from elli_runtime import errors

class HTTPResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

class FunctionReturn(Exception):
    def __init__(self, value):
        self.value = value
        self.function_depth = 0

class LoopBreak(Exception):
    pass

class ProgramTerminate(Exception):
    pass

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.scopes = [{}]
        self.loop_depth = 0
        self.function_depth = 0
        self.modules = {}

    def visit_AssignmentNode(self, node):
        value = self.visit(node.value)
        value_type = self.get_elli_type(value)

        for scope in reversed(self.scopes):

            if node.name in scope:
                var_type = scope[node.name]["type"]

                if scope[node.name].get("constant", False):
                    if errors.CURRENT_EDITION == "EN":
                        message = f"Modification of constant '{node.name}' is not allowed"
                    else:
                        message = f"Μη επιτρεπτή τροποποίηση ΣΤΑΘΕΡΑΣ '{node.name}'"

                    raise ELLIError("ΣΦΑΛΜΑ_ΤΥΠΟΥ", 0, message)

                # Δεν επιτρέπεται αλλαγή τύπου
                if var_type != value_type:

                    # Ειδικός κανόνας: ΚΕΝΟ δεν επιτρέπεται σε αριθμητικούς τύπους
                    numeric_types = ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ")

                    # Αν είναι ΑΡΙΘΜΟΣ → δέχεται και ΑΚΕΡΑΙΟΣ και ΔΕΚΑΔΙΚΟΣ
                    if var_type == "ΑΡΙΘΜΟΣ" and value_type in numeric_types:
                        scope[node.name]["value"] = value
                        return

                    # Αν είναι ΑΚΕΡΑΙΟΣ → πρέπει να είναι ακριβώς ΑΚΕΡΑΙΟΣ
                    if var_type == "ΑΚΕΡΑΙΟΣ" and value_type == "ΑΚΕΡΑΙΟΣ":
                        scope[node.name]["value"] = value
                        return

                    # Αν είναι ΔΕΚΑΔΙΚΟΣ → πρέπει να είναι ακριβώς ΔΕΚΑΔΙΚΟΣ
                    if var_type == "ΔΕΚΑΔΙΚΟΣ" and value_type == "ΔΕΚΑΔΙΚΟΣ":
                        scope[node.name]["value"] = value
                        return

                    # Για όλους τους άλλους τύπους
                    if var_type != value_type:
                        raise ELLITypeError(0,var_type, value_type)

                    scope[node.name]["value"] = value
                    return

                scope[node.name]["value"] = value
                return

        # Αν δεν βρεθεί σε κανένα scope
        raise ELLINameError(0,node.name)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
        

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    # ---- Τύποι ----
    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_VarDeclNode(self, node):
        value = self.visit(node.value)
        var_type_token = node.var_type

        # Μετατροπή TokenType → Εσωτερικό String Type
        type_map = {
            TokenType.NUMBER_TYPE: "ΑΡΙΘΜΟΣ",
            TokenType.INTEGER_TYPE: "ΑΚΕΡΑΙΟΣ",
            TokenType.DECIMAL_TYPE: "ΔΕΚΑΔΙΚΟΣ",
            TokenType.TEXT_TYPE: "ΚΕΙΜΕΝΟ",
            TokenType.BOOLEAN_TYPE: "ΛΟΓΙΚΟΣ",
            TokenType.LIST_TYPE: "ΛΙΣΤΑ",
            TokenType.HTTP_RESPONSE_TYPE: "HTTP_ΑΠΑΝΤΗΣΗ",
            TokenType.STRUCT_TYPE: "ΔΟΜΗ",
        }

        if var_type_token not in type_map:
            raise ELLITypeError(0,"Γνωστός Τύπος", str(var_type_token))

        var_type = type_map[var_type_token]

        # Έλεγχος τύπου
        if var_type == "ΑΡΙΘΜΟΣ":
            if not isinstance(value, (int, float)):
                raise ELLITypeError(0,"ΑΡΙΘΜΟΣ", self.get_elli_type(value))

        elif var_type == "ΑΚΕΡΑΙΟΣ":
            if not isinstance(value, int):
                raise ELLITypeError(0,"ΑΚΕΡΑΙΟΣ", self.get_elli_type(value))

        elif var_type == "ΔΕΚΑΔΙΚΟΣ":
            if not isinstance(value, float):
                raise ELLITypeError(0,"ΔΕΚΑΔΙΚΟΣ", self.get_elli_type(value))

        elif var_type == "ΚΕΙΜΕΝΟ":
            if not isinstance(value, str):
                raise ELLITypeError(0,"ΚΕΙΜΕΝΟ", self.get_elli_type(value))

        elif var_type == "ΛΙΣΤΑ":
            if not isinstance(value, list):
                raise ELLITypeError(0,"ΛΙΣΤΑ", self.get_elli_type(value))
            
        elif var_type == "ΛΟΓΙΚΟΣ":
            if not isinstance(value, bool):
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(value))
        
        elif var_type == "ΔΟΜΗ":
            if not isinstance(value, dict):
                raise ELLITypeError(0,"ΔΟΜΗ", self.get_elli_type(value))
        
        elif var_type == "HTTP_ΑΠΑΝΤΗΣΗ":
            if not isinstance(value, HTTPResponse):
                raise ELLITypeError(0, "HTTP_ΑΠΑΝΤΗΣΗ", self.get_elli_type(value))

        else:
            raise ELLITypeError(0,"Γνωστός Τύπος", var_type)

        # Αποθήκευση με metadata
        self.scopes[-1][node.name] = {
            "type": var_type,
            "value": value
        }

    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)

    def visit_InputNode(self, node):
        message = self.visit(node.message)
        user_input = input(str(message) + " ").strip()

        if node.input_type == "ΚΕΙΜΕΝΟ":
            return user_input

        if node.input_type == "ΑΡΙΘΜΟΣ":
            try:
                if "." in user_input:
                    return float(user_input)
                return int(user_input)
            except:
                raise ELLITypeError(0,"ΑΡΙΘΜΟΣ", "Μη αριθμητική είσοδος")

        if node.input_type == "ΛΟΓΙΚΟΣ":

            if user_input.upper() == "ΑΛΗΘΗΣ":
                return True

            if user_input.upper() == "ΨΕΥΔΗΣ":
                return False

            raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", "Μη λογική είσοδος")

        raise ELLITypeError(0,"Έγκυρος τύπος εισόδου", node.input_type)

    def visit_BinOpNode(self, node):
        # ----- ΛΟΓΙΚΟΙ ΤΕΛΕΣΤΕΣ -----
        if node.op == "ΚΑΙ":
            left = self.visit(node.left)

            if self.get_elli_type(left) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(left))
            # short-circuit
            if not left:
                return False

            right = self.visit(node.right)
            if self.get_elli_type(right) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(right))
            return right

        if node.op == "Ή":
            left = self.visit(node.left)
            if self.get_elli_type(left) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(left))

            # short-circuit
            if left:
                return True

            right = self.visit(node.right)
            if self.get_elli_type(right) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(right))

            return right

        if node.op == "ΟΧΙ":
            value = self.visit(node.left)

            if self.get_elli_type(value) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,"ΛΟΓΙΚΟΣ", self.get_elli_type(value))
            return not value
        
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == TokenType.PLUS:
            left_type = self.get_elli_type(left)
            right_type = self.get_elli_type(right)
            # ΚΕΙΜΕΝΟ με οτιδήποτε → επιτρέπεται
            if left_type == "ΚΕΙΜΕΝΟ" or right_type == "ΚΕΙΜΕΝΟ":
                return str(left) + str(right)
            # ΑΡΙΘΜΟΣ με ΑΡΙΘΜΟΣ → επιτρέπεται
            if left_type in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ") and \
            right_type in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                return left + right
            # Οτιδήποτε άλλο → TypeError
            raise ELLITypeError(0,
                f"Πρόσθεση {left_type} με {right_type}",
                "Μη συμβατός συνδυασμός τύπων"
            )
        if node.op in (TokenType.MINUS, TokenType.MUL, TokenType.DIV):
            left_type = self.get_elli_type(left)
            right_type = self.get_elli_type(right)

            if not (
                left_type in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ") and
                right_type in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ")
            ):
                raise ELLITypeError(0,
                    f"Πρόσθεση {left_type} με {right_type}",
                    "Μη συμβατός συνδυασμός τύπων"
                )
            if node.op == TokenType.MINUS:
                return left - right
            if node.op == TokenType.MUL:
                return left * right
            if node.op == TokenType.DIV:
                if right == 0:
                    raise ELLIZeroDivisionError(0)
                return left / right

        #raise Exception(f"Άγνωστη πράξη {node.op}")

    # ---- Loops ----
    def visit_WhileNode(self, node):
        self.loop_depth += 1
        try:
            while True:
                condition_value = self.visit(node.condition)

                # Αυστηρός έλεγχος τύπου
                if self.get_elli_type(condition_value) != "ΛΟΓΙΚΟΣ":
                    raise ELLITypeError(0,
                        "ΛΟΓΙΚΟΣ",
                        self.get_elli_type(condition_value)
                    )
                if not condition_value:
                    break

                self.scopes.append({})

                try:
                    for stmt in node.body:
                        self.visit(stmt)
                except LoopBreak:
                    self.scopes.pop()
                    break

                self.scopes.pop()

        finally:
            self.loop_depth -= 1

    def visit_ForNode(self, node):

        start = self.visit(node.start)
        end = self.visit(node.end)
        if not isinstance(start, int) or not isinstance(end, int):
            raise ELLITypeError(0,"ΑΚΕΡΑΙΟΣ", "Μη αριθμητικό όριο ΓΙΑ")

        self.loop_depth += 1

        try:
            for i in range(start, end + 1):

                self.scopes.append({})
                self.scopes[-1][node.var_name] = {
                    "type": "ΑΡΙΘΜΟΣ",
                    "value": i
                }

                try:
                    for stmt in node.body:
                        self.visit(stmt)
                except LoopBreak:
                    self.scopes.pop()
                    break

                self.scopes.pop()

        finally:
            self.loop_depth -= 1

    def visit_ForEachNode(self, node):
        collection = self.visit(node.collection)

        if not isinstance(collection, list):
            raise ELLITypeError(
                0,
                "ΛΙΣΤΑ",
                self.get_elli_type(collection)
            )

        self.loop_depth += 1

        try:
            for item in collection:

                self.scopes.append({})
                self.scopes[-1][node.var_name] = {
                    "type": self.get_elli_type(item),
                    "value": item
                }

                try:
                    for stmt in node.body:
                        self.visit(stmt)
                except LoopBreak:
                    self.scopes.pop()
                    break

                self.scopes.pop()

        finally:
            self.loop_depth -= 1

    # ---- If / Else ----
    def visit_IfNode(self, node):

        # ---- IF ----
        condition_value = self.visit(node.condition)

        if self.get_elli_type(condition_value) != "ΛΟΓΙΚΟΣ":
            raise ELLITypeError(0,
                "ΛΟΓΙΚΟΣ",
                self.get_elli_type(condition_value)
            )
        if condition_value:
            for stmt in node.body:
                self.visit(stmt)
            return

        # ---- ELIF ----
        for cond, body in node.elif_blocks:
            cond_value = self.visit(cond)

            if self.get_elli_type(cond_value) != "ΛΟΓΙΚΟΣ":
                raise ELLITypeError(0,
                    "ΛΟΓΙΚΟΣ",
                    self.get_elli_type(cond_value)
                )
            if cond_value:
                for stmt in body:
                    self.visit(stmt)
                return

        # ---- ELSE ----
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    # ---- Συναρτήσεις ----
    def visit_FuncDefNode(self, node):

        # αποθήκευση συνάρτησης
        self.functions[node.name] = node


    # ---- Λίστες ----
    def visit_ListNode(self, node):
        values = []

        for element in node.elements:
            values.append(self.visit(element))

        return values

    def visit_ListAppendNode(self, node):

        for scope in reversed(self.scopes):
            if node.list_name in scope:

                lst = scope[node.list_name]["value"]
                lst.append(self.visit(node.value))
                return

        raise ELLINameError(0, node.list_name)

    def visit_ListLengthNode(self, node):
        for scope in reversed(self.scopes):
            if node.list_name in scope:
                value = scope[node.list_name]["value"]
                value_type = self.get_elli_type(value)

                if value_type in ("ΛΙΣΤΑ", "ΔΟΜΗ"):
                    return len(value)
                
                # Numeric unification για error message
                if value_type in ("ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    value_type = "ΑΡΙΘΜΟΣ"

                raise ELLITypeError(
                    0, 
                    "ΛΙΣΤΑ ή ΔΟΜΗ", 
                    value_type
                )

        raise ELLINameError(0, node.list_name)
    
    def visit_VarAccessNode(self, node):
        for scope in reversed(self.scopes):
            if node.name in scope:
                return scope[node.name]["value"]
        raise ELLINameError(0,node.name)
    
    def visit_ComparisonNode(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        left_type = self.get_elli_type(left)
        right_type = self.get_elli_type(right)

        # --- ΚΕΝΟ ---
        if left_type == "ΚΕΝΟ" or right_type == "ΚΕΝΟ":
            if node.op not in (TokenType.EQ, TokenType.NE):
                raise ELLITypeError(0, left_type, right_type)
            return left == right

        # --- Numeric grouping ---
        if self.is_numeric(left) and self.is_numeric(right):

            if node.op == TokenType.EQ:
                return left == right
            if node.op == TokenType.NE:
                return left != right
            if node.op == TokenType.GT:
                return left > right
            if node.op == TokenType.LT:
                return left < right
            if node.op == TokenType.GTE:
                return left >= right
            if node.op == TokenType.LTE:
                return left <= right

        # --- Ίδιος τύπος ---
        if left_type == right_type:

            # ❗ Απαγορεύεται σύγκριση ΔΟΜΗΣ
            if left_type == "ΔΟΜΗ":
                if errors.CURRENT_EDITION == "EN":
                    expected = "STRUCT comparison is not allowed"
                    given = "Use explicit field comparison"
                else:
                    expected = "Μη επιτρεπτή σύγκριση ΔΟΜΩΝ"
                    given = "Χρησιμοποιήστε ρητή σύγκριση πεδίων"

                raise ELLITypeError(0, expected, given)
            if node.op == TokenType.EQ:
                return left == right
            if node.op == TokenType.NE:
                return left != right

            # > < επιτρέπονται μόνο για αριθμούς
            raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", left_type)

        # --- Διαφορετικοί τύποι ---
        raise ELLITypeError(0, left_type, right_type)

    def visit_FunctionCallNode(self, node):

        func = self.functions.get(node.name)
        if not func:
            raise ELLINameError(0,node.name)

        params = func.params
        body = func.body

        # νέο scope για την συνάρτηση
        local_scope = {}

        for i in range(len(params)):
            local_scope[params[i]] = {
                "type": "ΑΡΙΘΜΟΣ",
                "value": self.visit(node.args[i])
            }

        # push scope
        self.scopes.append(local_scope)
        self.function_depth += 1
        try:
            for stmt in body:
                self.visit(stmt)
        except FunctionReturn as ret:
            self.function_depth -= 1
            self.scopes.pop()
            return ret.value

        # αν δεν έγινε ΕΠΙΣΤΡΕΨΕ
        self.function_depth -= 1   # ✅ ΒΓΑΙΝΕΙ ΑΠΟ ΣΥΝΑΡΤΗΣΗ
        self.scopes.pop()
        return None


    def visit_ListAccessNode(self, node):

        container = self.visit(node.container)
        index = self.visit(node.index)
        container_type = self.get_elli_type(container)

        # --- ΛΙΣΤΑ ---
        if isinstance(container, list):
            if not isinstance(index, int):
                raise ELLITypeError(
                    0,
                    "ΑΚΕΡΑΙΟΣ",
                    self.get_elli_type(index)
                )

            if index < 0 or index >= len(container):
                raise ELLIError(
                    "ΣΦΑΛΜΑ_ΚΛΕΙΔΙΟΥ",
                    0,
                    "Μη έγκυρος δείκτης λίστας"
                )

            return container[index]

        # --- ΔΟΜΗ ---
        if isinstance(container, dict):

            if not isinstance(index, str):
                raise ELLITypeError(
                    0,
                    "ΚΕΙΜΕΝΟ",
                    self.get_elli_type(index)
                )

            if index not in container:
                raise ELLIKeyError(0, index)

            return container[index]
        
        # Άλλος τύπος
        raise ELLITypeError(
            0,
            "ΛΙΣΤΑ ή ΔΟΜΗ",
            container_type
        )
    
    def visit_CommentNode(self, node):
        pass

    def visit_ReturnNode(self, node):
        value = self.visit(node.value)
        if self.function_depth == 0:
            if errors.CURRENT_EDITION == "EN":
                message = "RETURN is only allowed inside a function"
            else:
                message = "Το ΕΠΙΣΤΡΕΨΕ επιτρέπεται μόνο μέσα σε συνάρτηση"

            raise ELLIBlockError(
                "ΣΦΑΛΜΑ_ΜΠΛΟΚ",
                0,
                message
            )
        raise FunctionReturn(value)
    
    def visit_BreakNode(self, node):
        if self.loop_depth == 0:
            if errors.CURRENT_EDITION == "EN":
                message = "BREAK is only allowed inside a loop"
            else:
                message = "Το ΔΙΑΚΟΨΕ επιτρέπεται μόνο μέσα σε βρόχο"

            raise ELLIBlockError(
                "ΣΦΑΛΜΑ_ΜΠΛΟΚ",
                0,
                message
            )
        raise LoopBreak()

    def visit_LoopBreakNode(self, node):
        if self.loop_depth == 0:
            raise ELLISyntaxError(
                0,
                "Η ΔΙΑΚΟΠΗ επιτρέπεται μόνο μέσα σε loop"
                if errors.CURRENT_EDITION != "EN"
                else "LOOP_BREAK is only allowed inside a loop"
            )

        raise LoopBreak()

    def visit_TerminateNode(self, node):
        raise ProgramTerminate()
    
    def get_elli_type(self, value):
        # --- NULL ---
        if value is None:
            return "ΚΕΝΟ"
        # --- BOOLEAN ---
        if isinstance(value, bool):
            return "ΛΟΓΙΚΟΣ"
        # --- INTEGER ---
        if isinstance(value, int):
            return "ΑΚΕΡΑΙΟΣ"
        # --- FLOAT ---
        if isinstance(value, float):
            return "ΔΕΚΑΔΙΚΟΣ"
        # --- STRING ---
        if isinstance(value, str):
            return "ΚΕΙΜΕΝΟ"
        # --- LIST ---
        if isinstance(value, list):
            return "ΛΙΣΤΑ"
        if isinstance(value, dict):
            return "ΔΟΜΗ"
        if isinstance(value, HTTPResponse):
            return "HTTP_ΑΠΑΝΤΗΣΗ"
        if errors.CURRENT_EDITION == "EN":
            message = f"Unknown internal type: {type(value)}"
        else:
            message = f"Άγνωστος εσωτερικός τύπος: {type(value)}"

        raise Exception(message)
    
    def visit_BooleanNode(self, node):
        return node.value
    
    def visit_ToBooleanNode(self, node):
        value = self.visit(node.expression)

        # Ήδη λογικός
        if isinstance(value, bool):
            return value
        # Αριθμοί
        if isinstance(value, (int, float)):
            return value != 0
        # Κείμενο
        if isinstance(value, str):
            return value != ""
        # ΚΕΝΟ (None)
        if value is None:
            return False

        expected = "Non-convertible type to BOOLEAN" if errors.CURRENT_EDITION == "EN" else "Μη μετατρέψιμος τύπος σε ΛΟΓΙΚΟΣ"
        raise ELLITypeError(0, expected, self.get_elli_type(value))
    
    def visit_NullNode(self, node):
        return None
    
    def visit_NotNode(self, node):
        value = self.visit(node.expression)

        if self.get_elli_type(value) != "ΛΟΓΙΚΟΣ":
            raise ELLITypeError(0,
                "ΛΟΓΙΚΟΣ",
                self.get_elli_type(value)
            )
        return not value
    
    def is_numeric(self, value):
        return self.get_elli_type(value) in ("ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ")
    
    def visit_NamespaceCallNode(self, node):
        namespace = node.namespace
        function = node.function
        args = [self.visit(arg) for arg in node.args]

        # ---- MODULE NAMESPACE ----
        if hasattr(self, "modules") and node.namespace in self.modules:

            module_data = self.modules[node.namespace]

            # Function call
            if node.function in module_data["functions"]:

                func_node = module_data["functions"][node.function]
                args = [self.visit(arg) for arg in node.args]

                # νέο scope με module variables
                local_scope = dict(module_data["variables"])

                for i in range(len(func_node.params)):
                    local_scope[func_node.params[i]] = {
                        "type": "ΑΡΙΘΜΟΣ",
                        "value": args[i]
                    }

                self.scopes.append(local_scope)
                self.function_depth += 1
                try:
                    for stmt in func_node.body:
                        self.visit(stmt)
                except FunctionReturn as ret:
                    self.function_depth -= 1
                    self.scopes.pop()
                    return ret.value
                
                self.function_depth -= 1
                self.scopes.pop()
                return None

            # Variable access
            if node.function in module_data["variables"]:
                return module_data["variables"][node.function]["value"]

            from .errors import ELLINameError
            raise ELLINameError(0, node.function)

        # FILE / ΑΡΧΕΙΟ namespace
        if namespace in ("ΑΡΧΕΙΟ", "FILE"):
            # -------- READ --------
            if function in ("ΑΝΑΓΝΩΣΕ", "READ"):
                if len(args) != 1:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ",
                        0,
                        "READ requires 1 argument" if errors.CURRENT_EDITION == "EN" else "Η ΑΝΑΓΝΩΣΕ/READ απαιτεί 1 όρισμα"
                    )
                if self.get_elli_type(args[0]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[0]))

                filename = args[0]

                try:
                    with open(filename, "r", encoding="utf8") as f:
                        return f.read()
                except Exception:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΕΙΣΟΔΟΥ_ΕΞΟΔΟΥ",
                        0,
                        f"Αποτυχία ανάγνωσης αρχείου '{filename}'"
                    )
            # -------- WRITE --------
            if function in ("ΓΡΑΨΕ", "WRITE"):
                if len(args) != 2:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ",
                        0,
                        "Η ΓΡΑΨΕ/WRITE απαιτεί 2 ορίσματα"
                    )
                if self.get_elli_type(args[0]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[0]))

                if self.get_elli_type(args[1]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[1]))

                filename = args[0]
                content = args[1]

                try:
                    with open(filename, "w", encoding="utf8") as f:
                        f.write(content)
                    return None
                except Exception:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΕΙΣΟΔΟΥ_ΕΞΟΔΟΥ",
                        0,
                        f"Αποτυχία εγγραφής αρχείου '{filename}'"
                    )
        # FILE JSON
        elif namespace == "JSON":
            #ΑΠΟ_ΚΕΙΜΕΝΟ
            if function in ("ΑΠΟ_ΚΕΙΜΕΝΟ", "FROM_TEXT"):

                if len(args) != 1:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ",
                        0,
                        "Η ΑΠΟ_ΚΕΙΜΕΝΟ απαιτεί 1 όρισμα"
                    )

                value = args[0]

                # ΠΡΩΤΑ αυστηρός έλεγχος τύπου
                if not isinstance(value, str):
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(value))

                try:
                    return json.loads(value)
                except Exception:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_JSON",
                        0,
                        f"Μη έγκυρο JSON: {value}"
                    )
            
            #ΣΕ_ΚΕΙΜΕΝΟ
            if function in ("ΣΕ_ΚΕΙΜΕΝΟ", "TO_TEXT"):

                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΣΕ_ΚΕΙΜΕΝΟ απαιτεί 1 όρισμα")

                try:
                    return json.dumps(args[0], ensure_ascii=False)
                except:
                    raise ELLIError("ΣΦΑΛΜΑ_JSON", 0, "Αποτυχία μετατροπής σε JSON")
            #ΦΟΡΤΩΣΕ
            if function in ("ΦΟΡΤΩΣΕ", "LOAD"):
                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΦΟΡΤΩΣΕ απαιτεί 1 όρισμα")

                if self.get_elli_type(args[0]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[0]))

                try:
                    with open(args[0], "r", encoding="utf8") as f:
                        data = json.load(f)
                except:
                    raise ELLIError("ΣΦΑΛΜΑ_ΕΙΣΟΔΟΥ_ΕΞΟΔΟΥ", 0, "Αποτυχία φόρτωσης JSON")

                return data
            #ΑΠΟΘΗΚΕΥΣΕ
            if function in ("ΑΠΟΘΗΚΕΥΣΕ", "SAVE"):
                if len(args) != 2:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΑΠΟΘΗΚΕΥΣΕ απαιτεί 2 ορίσματα")

                if self.get_elli_type(args[1]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[1]))

                try:
                    with open(args[1], "w", encoding="utf8") as f:
                        json.dump(args[0], f, ensure_ascii=False)
                    return None
                except:
                    raise ELLIError("ΣΦΑΛΜΑ_ΕΙΣΟΔΟΥ_ΕΞΟΔΟΥ", 0, "Αποτυχία αποθήκευσης JSON")
        elif namespace == "HTTP":
            #GET Implementation
            if function in ("GET",):

                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η GET απαιτεί 1 όρισμα")

                if self.get_elli_type(args[0]) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(args[0]))

                import urllib.request

                try:
                    with urllib.request.urlopen(args[0]) as response:
                        status = response.getcode()
                        body = response.read().decode("utf8")
                        return HTTPResponse(status, body)
                except:
                    raise ELLIError("ΣΦΑΛΜΑ_HTTP", 0, "Αποτυχία HTTP GET")
            #POST Implementation
            if function in ("POST",):

                if len(args) != 2:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η POST απαιτεί 2 ορίσματα")

                url = args[0]
                data = args[1]

                if self.get_elli_type(url) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(url))

                import urllib.request

                if self.get_elli_type(data) == "ΛΙΣΤΑ":
                    data = json.dumps(data).encode("utf8")
                elif self.get_elli_type(data) == "ΚΕΙΜΕΝΟ":
                    data = data.encode("utf8")
                else:
                    raise ELLITypeError(0, "ΚΕΙΜΕΝΟ ή ΛΙΣΤΑ", self.get_elli_type(data))

                try:
                    req = urllib.request.Request(url, data=data, method="POST")
                    with urllib.request.urlopen(req) as response:
                        status = response.getcode()
                        body = response.read().decode("utf8")
                        return HTTPResponse(status, body)
                except:
                    raise ELLIError("ΣΦΑΛΜΑ_HTTP", 0, "Αποτυχία HTTP POST")
            #STATUS
            if function in ("ΚΩΔΙΚΟΣ", "STATUS"):

                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΚΩΔΙΚΟΣ απαιτεί 1 όρισμα")

                if not isinstance(args[0], HTTPResponse):
                    raise ELLITypeError(0, "HTTP_ΑΠΑΝΤΗΣΗ", self.get_elli_type(args[0]))

                return args[0].status_code
            #BODY
            if function in ("ΣΩΜΑ", "BODY"):
                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΣΩΜΑ απαιτεί 1 όρισμα")
                if not isinstance(args[0], HTTPResponse):
                    raise ELLITypeError(0, "HTTP_ΑΠΑΝΤΗΣΗ", self.get_elli_type(args[0]))

                return args[0].body
            
        elif namespace in ("ΔΟΜΗ", "STRUCT"):
            # ΠΕΡΙΕΧΕΙ
            if function in ("ΠΕΡΙΕΧΕΙ", "CONTAINS"):
                if len(args) != 2:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ",
                        0,
                        "Η ΠΕΡΙΕΧΕΙ απαιτεί 2 ορίσματα"
                    )
                struct = args[0]
                key = args[1]

                #Έλεγχος 1ου ορίσματος
                if self.get_elli_type(struct) != "ΔΟΜΗ":
                    given_type = self.get_elli_type(struct)
                    # Αν είναι αριθμητικό subtype → εμφάνισε ΑΡΙΘΜΟΣ
                    if given_type in ("ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                        given_type = "ΑΡΙΘΜΟΣ"

                    raise ELLITypeError(
                        0, 
                        "ΔΟΜΗ", 
                        given_type
                    )
                #Έλεγχος 2ου ορίσματος
                if self.get_elli_type(key) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(
                        0, 
                        "ΚΕΙΜΕΝΟ", 
                        self.get_elli_type(key)
                    )

                return key in struct

            # ΔΙΑΓΡΑΨΕ
            if function in ("ΔΙΑΓΡΑΨΕ", "DELETE"):
                if len(args) != 2:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 
                        0, 
                        "Η ΔΙΑΓΡΑΨΕ απαιτεί 2 ορίσματα"
                    )

                struct = args[0] 
                key = args[1]

                #Έλεγχος 1ου ορίσματος
                if self.get_elli_type(struct) != "ΔΟΜΗ":
                    given_type = self.get_elli_type(struct)

                    if given_type in ("ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                        given_type = "ΑΡΙΘΜΟΣ"
                    raise ELLITypeError(
                        0, 
                        "ΔΟΜΗ", 
                        given_type
                    )
                #Έλεγχος 2ου ορίσματος
                if self.get_elli_type(key) != "ΚΕΙΜΕΝΟ":
                    raise ELLITypeError(
                        0,
                        "ΚΕΙΜΕΝΟ",
                        self.get_elli_type(key)
                    )
                
                #Έλεγχος ύπαρξης κλειδιού
                if key not in struct:
                    raise ELLIKeyError(0, key)
                del struct[key]
                return None

            # ΚΛΕΙΔΙΑ
            if function in ("ΚΛΕΙΔΙΑ", "KEYS"):

                if len(args) != 1:
                    raise ELLIError(
                        "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 
                        0, 
                        "Η ΚΛΕΙΔΙΑ απαιτεί 1 όρισμα"
                    )

                struct = args[0]
                struct_type = self.get_elli_type(struct)

                if struct_type != "ΔΟΜΗ":
                    if struct_type in ("ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                        struct_type = "ΑΡΙΘΜΟΣ"
                    raise ELLITypeError(
                        0, 
                        "ΔΟΜΗ", 
                        struct_type
                    )
                # Python 3.7+ διατηρεί insertion order
                keys = list(struct.keys())
                # Επιβεβαίωση ότι όλα είναι ΚΕΙΜΕΝΟ (ασφάλεια runtime)
                for k in keys:
                    if not isinstance(k, str):
                        raise ELLITypeError(
                            0,
                            "ΚΕΙΜΕΝΟ",
                            self.get_elli_type(k)
                        )

                return keys

        # ---- MATH NAMESPACE ----
        elif namespace in ("ΜΑΘ", "MATH"):

            # ΤΕΤΡΑΓΩΝΟ / SQUARE
            if function in ("ΤΕΤΡΑΓΩΝΟ", "SQUARE"):
                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΤΕΤΡΑΓΩΝΟ απαιτεί 1 όρισμα")

                value = args[0]
                if self.get_elli_type(value) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(value))

                return value * value
            
            # ΡΙΖΑ / SQRT
            if function in ("ΡΙΖΑ", "SQRT"):
                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΡΙΖΑ απαιτεί 1 όρισμα")

                value = args[0]
                if self.get_elli_type(value) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(value))

                import math
                return math.sqrt(value)
            
            #ΕΛΑΧΙΣΤΟ / MIN
            if function in ("ΕΛΑΧΙΣΤΟ", "MIN"):
                if len(args) != 2:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΕΛΑΧΙΣΤΟ απαιτεί 2 ορίσματα")

                a, b = args

                if self.get_elli_type(a) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(a))

                if self.get_elli_type(b) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(b))

                return min(a, b)
            
            #ΜΕΓΙΣΤΟ / MAX
            if function in ("ΜΕΓΙΣΤΟ", "MAX"):
                if len(args) != 2:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΜΕΓΙΣΤΟ απαιτεί 2 ορίσματα")

                a, b = args

                if self.get_elli_type(a) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(a))

                if self.get_elli_type(b) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(b))

                if errors.CURRENT_EDITION == "EN":
                    return max(a, b)
                else:
                    return max(a, b)
                
            # ΑΠΟΛΥΤΗ / ABS
            if function in ("ΑΠΟΛΥΤΗ", "ABS"):
                if len(args) != 1:
                    raise ELLIError("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", 0, "Η ΑΠΟΛΥΤΗ απαιτεί 1 όρισμα")

                value = args[0]

                if self.get_elli_type(value) not in ("ΑΡΙΘΜΟΣ", "ΑΚΕΡΑΙΟΣ", "ΔΕΚΑΔΙΚΟΣ"):
                    raise ELLITypeError(0, "ΑΡΙΘΜΟΣ", self.get_elli_type(value))

                return abs(value)
            
        # Unknown namespace
        if errors.CURRENT_EDITION == "EN":
            message = f"Unknown namespace '{namespace}'"
        else:
            message = f"Άγνωστο namespace '{namespace}'"

        raise ELLIError(
            "ΣΦΑΛΜΑ_ΟΝΟΜΑΤΟΣ",
            0,
            message
        )
    
    def visit_StructNode(self, node):
        result = {}

        for key_node, value_node in node.pairs:
            key = self.visit(key_node)

            if not isinstance(key, str):
                raise ELLITypeError(0, "ΚΕΙΜΕΝΟ", self.get_elli_type(key))

            value = self.visit(value_node)

            allowed_types = (int, float, str, bool, list, dict)

            if value is not None and not isinstance(value, allowed_types):
                raise ELLITypeError(
                    0,
                    "ΑΡΙΘΜΟΣ, ΚΕΙΜΕΝΟ, ΛΟΓΙΚΟΣ, ΛΙΣΤΑ, ΔΟΜΗ ή ΚΕΝΟ",
                    self.get_elli_type(value)
                )
            result[key] = value

        return result
    
    def visit_StructAssignmentNode(self, node):
        # Βρες τη μεταβλητή στο scope
        for scope in reversed(self.scopes):
            if node.name in scope:

                container = scope[node.name]["value"]
                container_type = scope[node.name]["type"]

                # Πρέπει να είναι ΔΟΜΗ
                if not isinstance(container, dict):  #ΔΟΜΗ
                    raise ELLITypeError(
                        0,
                        "ΔΟΜΗ",
                        self.get_elli_type(container)
                    )
                
                # Αξιολόγηση κλειδιού
                key = self.visit(node.key)
                if not isinstance(key, str):
                    raise ELLITypeError(
                        0,
                        "ΚΕΙΜΕΝΟ",
                        self.get_elli_type(key)
                    )

                # Αξιολόγηση τιμής
                value = self.visit(node.value)
                allowed_types = (int, float, str, bool, list, dict, type(None))

                if not isinstance(value, allowed_types):
                    raise ELLITypeError(
                        0,
                        "ΑΡΙΘΜΟΣ, ΚΕΙΜΕΝΟ, ΛΟΓΙΚΟΣ, ΛΙΣΤΑ, ΔΟΜΗ ή ΚΕΝΟ",
                        self.get_elli_type(value)
                    )
                
                # Δημιουργία ή αντικατάσταση
                container[key] = value
                return
            
        # Αν δεν βρεθεί η μεταβλητή
        raise ELLINameError(0, node.name)

    def visit_ConstDeclNode(self, node):
        value = self.visit(node.value)

        # reuse VarDecl logic για type validation
        fake_node = VarDeclNode(node.name, node.var_type, node.value)
        self.visit_VarDeclNode(fake_node)

        # Μαρκάρουμε ως constant
        self.scopes[-1][node.name]["constant"] = True