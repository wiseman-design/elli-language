from .tokens import TokenType
from .ast_nodes import *
from .errors import ELLISyntaxError
from elli_runtime import errors

class ExpressionParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            if errors.CURRENT_EDITION == "EN":
                message = f"Expected {token_type.name}"
            else:
                message = f"Αναμενόταν {token_type.name}"

            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                message
            )
    
    def skip_newlines(self):
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()

    # expression -> comparison
    def parse(self):
        node = self.or_expr()
        return node

    # or_expr -> and_expr ( Ή and_expr )*
    def or_expr(self):
        node = self.and_expr()

        while self.current_token and self.current_token.type == TokenType.OR:
            op = self.current_token
            self.advance()
            right = self.and_expr()
            node = BinOpNode(node, op.value, right)

        return node

    # and_expr -> not_expr ( ΚΑΙ not_expr )*
    def and_expr(self):
        node = self.not_expr()

        while self.current_token and self.current_token.type == TokenType.AND:
            op = self.current_token
            self.advance()
            right = self.not_expr()
            node = BinOpNode(node, op.value, right)

        return node

    # not_expr -> ΟΧΙ not_expr | comparison
    def not_expr(self):
        if self.current_token and self.current_token.type == TokenType.NOT:
            self.advance()
            expr = self.not_expr()
            return NotNode(expr)

        return self.comparison()

    # comparison -> term ((== | != | > | < | >= | <=) term)*
    def comparison(self):
        node = self.term()

        while self.current_token and self.current_token.type in (
            TokenType.EQ,
            TokenType.NE,
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
        ):
            op = self.current_token
            self.advance()
            right = self.term()
            node = ComparisonNode(node, op.type, right)

        return node

    # term -> factor ((+ | -) factor)*
    def term(self):
        node = self.factor()

        while self.current_token and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = BinOpNode(node, op.type, right)

        return node

    # factor -> unary ((* | /) unary)*
    def factor(self):
        node = self.unary()

        while self.current_token and self.current_token.type in (
            TokenType.MUL,
            TokenType.DIV,
        ):
            op = self.current_token
            self.advance()
            right = self.unary()
            node = BinOpNode(node, op.type, right)

        return node

    # unary -> primary
    def unary(self):

        # NOT (ΟΧΙ)
        if (
            self.current_token
            and self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == "ΟΧΙ"
        ):
            self.advance()
            expr = self.unary()
            return NotNode(expr)

        # 🔥 NEW: Unary minus
        if self.current_token and self.current_token.type == TokenType.MINUS:
            self.advance()
            expr = self.unary()
            return BinOpNode(NumberNode(0), TokenType.MINUS, expr)

        return self.primary()

    # primary -> NUMBER | STRING | IDENTIFIER | "(" expression ")"
    def primary(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token.value)

        if token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringNode(token.value)
        
        if token.type == TokenType.LIST_LENGTH:
            self.advance()
            self.eat(TokenType.LPAREN)

            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.RPAREN)

            return ListLengthNode(name)

        # ΠΕΣ_ΜΟΥ: "μήνυμα"
        if token.type == TokenType.INPUT:
            self.advance()
            input_type = "ΚΕΙΜΕΝΟ"

            # Namespace μορφή
            if self.current_token and self.current_token.type == TokenType.DOT:
                self.advance()

                if self.current_token.type in (
                    TokenType.TEXT_TYPE,
                    TokenType.NUMBER_TYPE,
                    TokenType.BOOLEAN_TYPE
                ):
                    type_map = {
                        TokenType.TEXT_TYPE: "ΚΕΙΜΕΝΟ",
                        TokenType.NUMBER_TYPE: "ΑΡΙΘΜΟΣ",
                        TokenType.BOOLEAN_TYPE: "ΛΟΓΙΚΟΣ",
                        TokenType.STRUCT_TYPE: "ΔΟΜΗ"
                    }

                    input_type = type_map[self.current_token.type]
                    self.advance()
                else:
                    if errors.CURRENT_EDITION == "EN":
                        message = "Invalid type in INPUT"
                    else:
                        message = "Μη έγκυρος τύπος στο ΠΕΣ_ΜΟΥ"

                    raise ELLISyntaxError(
                        self.current_token.line,
                        message
                    )
            self.eat(TokenType.COLON)
            message_node = self.parse()

            return InputNode(message_node, input_type)

        if token.type in (
            TokenType.IDENTIFIER,
            TokenType.STRUCT_TYPE,
        ):
            namespace_or_name = token.value
            self.advance()

            # Namespace call
            if self.current_token and self.current_token.type == TokenType.DOT:
                self.advance()  # eat dot

                if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
                    if errors.CURRENT_EDITION == "EN":
                        message = "Expected name after namespace"
                    else:
                        message = "Αναμενόταν όνομα μετά το namespace"

                    raise ELLISyntaxError(
                        token.line,
                        message
                    )

                name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)

                # ---- Function Call ----
                if self.current_token and self.current_token.type == TokenType.LPAREN:

                    self.eat(TokenType.LPAREN)
                    self.skip_newlines()
                    args = []

                    if self.current_token and self.current_token.type != TokenType.RPAREN:
                        args.append(self.parse())
                        self.skip_newlines()

                        while self.current_token and self.current_token.type == TokenType.COMMA:
                            self.eat(TokenType.COMMA)
                            self.skip_newlines()
                            args.append(self.parse())
                            self.skip_newlines()

                    self.eat(TokenType.RPAREN)

                    return NamespaceCallNode(namespace_or_name, name, args)

                # ---- Variable Access ----
                return NamespaceCallNode(namespace_or_name, name, [])

            # ---- Function Call ----
            if self.current_token and self.current_token.type == TokenType.LPAREN:

                self.eat(TokenType.LPAREN)
                self.skip_newlines()
                args = []

                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse())
                    self.skip_newlines()

                    while self.current_token and self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        self.skip_newlines()
                        args.append(self.parse())
                        self.skip_newlines()

                self.eat(TokenType.RPAREN)

                return FunctionCallNode(namespace_or_name, args)

            # Access / Chained Access
            node = VarAccessNode(namespace_or_name)

            while self.current_token and self.current_token.type == TokenType.LBRACKET:
                self.eat(TokenType.LBRACKET)
                index = self.parse()
                self.eat(TokenType.RBRACKET)
                node = ListAccessNode(node, index)

            return node

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.skip_newlines()
            node = self.parse()
            self.skip_newlines()
            self.eat(TokenType.RPAREN)
            return node
        
        if token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            self.skip_newlines()
            elements = []

            if self.current_token and self.current_token.type != TokenType.RBRACKET:

                elements.append(self.parse())
                self.skip_newlines()

                while self.current_token and self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    self.skip_newlines()
                    elements.append(self.parse())
                    self.skip_newlines()

            self.eat(TokenType.RBRACKET)

            return ListNode(elements)
        
        if token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)

            pairs = []

            while self.current_token and self.current_token.type == TokenType.NEWLINE:
                self.advance()

            if self.current_token.type != TokenType.RBRACE:

                key = self.parse()

                while self.current_token.type == TokenType.NEWLINE:
                    self.advance()

                self.eat(TokenType.COLON)

                while self.current_token.type == TokenType.NEWLINE:
                    self.advance()

                value = self.parse()
                pairs.append((key, value))

                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)

                    while self.current_token.type == TokenType.NEWLINE:
                        self.advance()

                    key = self.parse()

                    while self.current_token.type == TokenType.NEWLINE:
                        self.advance()

                    self.eat(TokenType.COLON)

                    while self.current_token.type == TokenType.NEWLINE:
                        self.advance()

                    value = self.parse()
                    pairs.append((key, value))

            while self.current_token.type == TokenType.NEWLINE:
                self.advance()

            self.eat(TokenType.RBRACE)

            return StructNode(pairs)

        if token.type == TokenType.TRUE:
            self.advance()
            return BooleanNode(True)

        if token.type == TokenType.FALSE:
            self.advance()
            return BooleanNode(False)
        
        if token.type == TokenType.NULL:
            self.advance()
            return NullNode()

        if token.type == TokenType.TO_BOOLEAN:
            self.advance()
            self.eat(TokenType.LPAREN)
            expr = self.parse()
            self.eat(TokenType.RPAREN)
            return ToBooleanNode(expr)

        if errors.CURRENT_EDITION == "EN":
            message = f"Invalid expression: {token}"
        else:
            message = f"Μη έγκυρη έκφραση: {token}"

        raise Exception(message)
    
    @property
    def consumed(self):
        return self.pos