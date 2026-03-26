# Nodes για AST

class Node:
    pass


# Τύποι
class NumberNode(Node):
    def __init__(self, value):
        self.value = value


class StringNode(Node):
    def __init__(self, value):
        self.value = value


class VarDeclNode(Node):
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value

class ConstDeclNode(Node):
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value

class PrintNode(Node):
    def __init__(self, value):
        self.value = value


class InputNode(Node):
    def __init__(self, message, input_type="ΚΕΙΜΕΝΟ"):
        self.message = message
        self.input_type = input_type


# Loops
class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode(Node):
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.body = body


# If / Else
class IfNode(Node):
    def __init__(self, condition, body, elif_blocks=None, else_body=None):
        self.condition = condition
        self.body = body
        self.elif_blocks = elif_blocks or []
        self.else_body = else_body


# Συναρτήσεις
class FuncDefNode(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


# Λίστες
class ListNode(Node):
    def __init__(self, elements):
        self.elements = elements

class ListAccessNode(Node):
    def __init__(self, container, index):
        self.container = container
        self.index = index

class ListAppendNode(Node):
    def __init__(self, list_name, value):
        self.list_name = list_name
        self.value = value


class ListLengthNode(Node):
    def __init__(self, list_name):
        self.list_name = list_name


# Εκφράσεις
class VarAccessNode(Node):
    def __init__(self, name):
        self.name = name


class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class ComparisonNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class AssignmentNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class FunctionCallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class CommentNode(Node):
    def __init__(self, text):
        self.text = text

class ReturnNode:
    def __init__(self, value):
        self.value = value

class BooleanNode:
    def __init__(self, value):
        self.value = value

class ToBooleanNode:
    def __init__(self, expression):
        self.expression = expression

class NullNode(Node):
    pass

class BreakNode(Node):
    pass

class TerminateNode(Node):
    pass

class NotNode(Node):
    def __init__(self, expression):
        self.expression = expression

class NamespaceCallNode(Node):
    def __init__(self, namespace, function, args):
        self.namespace = namespace
        self.function = function
        self.args = args

class StructNode:
    def __init__(self, pairs):
        self.pairs = pairs  # list of (key_node, value_node)

class StructAssignmentNode:
    def __init__(self, name, key, value):
        self.name = name
        self.key = key
        self.value = value

class ImportNode(Node):
    def __init__(self, module_name):
        self.module_name = module_name

class FromImportNode(Node):
    def __init__(self, module_name, element_name):
        self.module_name = module_name
        self.element_name = element_name