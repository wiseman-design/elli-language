from .tokens import TokenType
from .ast_nodes import *
from .expression_parser import ExpressionParser
from .errors import ELLISyntaxError
from elli_runtime import errors

class StatementParser:
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

        if self.current_token is None:
            if errors.CURRENT_EDITION == "EN":
                message = "Unexpected end of file"
            else:
                message = "Απρόσμενο τέλος αρχείου"

            raise ELLISyntaxError(-1, message)

        if self.current_token.type == token_type:
            self.advance()
        else:
            if errors.CURRENT_EDITION == "EN":
                message = f"Expected {token_type.name} but found '{self.current_token.value}'"
            else:
                message = f"Αναμενόταν {token_type.name} αλλά βρέθηκε '{self.current_token.value}'"

            raise ELLISyntaxError(
                self.current_token.line,
                message
            )
        
    def skip_newlines(self):
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self):
        # Αγνόηση NEWLINE
        while (
            self.current_token
            and self.current_token.type == TokenType.NEWLINE
        ):
            self.advance()
            if self.current_token is None:
                return None

        # 🔥 ΠΡΩΤΟ ΑΠΟ ΟΛΑ
        # ---- Block terminators ----
        if self.current_token.type in (
            TokenType.END_IF,
            TokenType.END_FOR,
            TokenType.END_WHILE,
            TokenType.END_FUNCTION,
            TokenType.ELSE,
            TokenType.ELSE_IF
        ):
            return None
        # ---- Statements ----

        if self.current_token.type == TokenType.BREAK:
            self.eat(TokenType.BREAK)
            return BreakNode()
        
        if self.current_token.type == TokenType.LOOP_BREAK:
            self.advance()
            return LoopBreakNode()
        
        if self.current_token.type == TokenType.CONSTANT:
            return self.parse_const_decl()
        
        if self.current_token.type == TokenType.IMPORT:
            return self.parse_import()

        if self.current_token.type == TokenType.FROM:
            return self.parse_from_import()

        if self.current_token.type == TokenType.DECLARE:

            # έλεγχος αν είναι συνάρτηση
            if (
                self.pos + 3 < len(self.tokens)
                and self.tokens[self.pos + 2].type == TokenType.AS
                and self.tokens[self.pos + 3].type == TokenType.FUNCTION
            ):
                return self.parse_function()

            return self.parse_var_decl()

        if self.current_token.type == TokenType.DISPLAY:
            return self.parse_print()

        if self.current_token.type == TokenType.IF:
            return self.parse_if()

        if self.current_token.type == TokenType.FOR:
            return self.parse_for()

        if self.current_token.type == TokenType.WHILE:
            return self.parse_while()

        if self.current_token.type == TokenType.LIST_APPEND:
            return self.parse_list_append()

        if self.current_token.type == TokenType.COMMENT:
            return self.parse_comment()

        if self.current_token.type == TokenType.RETURN:
            return self.parse_return()

        if self.current_token.type == TokenType.TERMINATE:
            self.eat(TokenType.TERMINATE)
            return TerminateNode()

        # IDENTIFIER -> μπορεί να είναι function call ή assignment
        if self.current_token.type in (
            TokenType.IDENTIFIER,
            TokenType.STRUCT_TYPE,
        ):
            # Namespace call
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].type == TokenType.DOT
            ):
                expr_parser = ExpressionParser(self.tokens[self.pos:])
                node = expr_parser.parse()

                self.pos += expr_parser.consumed
                if self.pos < len(self.tokens):
                    self.current_token = self.tokens[self.pos]
                else:
                    self.current_token = None

                return node

            # function call
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].type == TokenType.LPAREN
            ):
                return self.parse_function_call()

            # assignment
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)

            # --- Struct Assignment ---
            if self.current_token and self.current_token.type == TokenType.LBRACKET:

                self.eat(TokenType.LBRACKET)

                expr_parser = ExpressionParser(self.tokens[self.pos:])
                key = expr_parser.parse()

                self.pos += expr_parser.consumed
                self.current_token = self.tokens[self.pos]

                self.eat(TokenType.RBRACKET)
                self.eat(TokenType.ASSIGN)

                expr_parser = ExpressionParser(self.tokens[self.pos:])
                value = expr_parser.parse()

                self.pos += expr_parser.consumed
                self.current_token = self.tokens[self.pos]

                return StructAssignmentNode(name, key, value)

            if self.current_token and self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)

                expr_parser = ExpressionParser(self.tokens[self.pos:])
                value = expr_parser.parse()

                # 🔥 ΑΥΤΟ ΠΡΟΣΘΕΤΕΙΣ
                self.pos += expr_parser.consumed
                self.current_token = self.tokens[self.pos]

                return AssignmentNode(name, value)

        # Αν τελειώσαμε τα tokens
        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None

        # Expression fallback
        expr_parser = ExpressionParser(self.tokens[self.pos:])
        node = expr_parser.parse()

        self.pos += expr_parser.consumed

        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        return node

    def parse_print(self):
        self.eat(TokenType.DISPLAY)  # ΕΜΦΑΝΙΣΕ
        self.eat(TokenType.COLON)

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        value = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        return PrintNode(value)

    def parse_if(self):

        self.eat(TokenType.IF)  # ΑΝ

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        condition = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        self.eat(TokenType.THEN)  # ΤΟΤΕ
        self.eat(TokenType.COLON)

        body = self.parse_block()

        elif_blocks = []
        else_body = None

        while self.current_token and self.current_token.type in (
            TokenType.ELSE_IF,
            TokenType.ELSE
        ):
            if self.current_token.type == TokenType.ELSE_IF:

                self.eat(TokenType.ELSE_IF)

                expr_parser = ExpressionParser(self.tokens[self.pos:])
                cond = expr_parser.parse()

                self.pos += expr_parser.consumed
                if self.pos < len(self.tokens):
                    self.current_token = self.tokens[self.pos]
                else:
                    self.current_token = None

                self.eat(TokenType.THEN)  # ΤΟΤΕ
                self.eat(TokenType.COLON)

                block = self.parse_block()
                elif_blocks.append((cond, block))

            elif self.current_token.type == TokenType.ELSE:

                self.eat(TokenType.ELSE)
                self.eat(TokenType.COLON)

                else_body = self.parse_block()
                break

            else:
                break
        
        if not self.current_token or self.current_token.type != TokenType.END_IF:
            if errors.CURRENT_EDITION == "EN":
                message = "Expected keyword 'END_IF'"
            else:
                message = "Αναμενόταν η λέξη-κλειδί 'ΤΕΛΟΣ_ΑΝ'"

            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                message
            )
        self.eat(TokenType.END_IF)  # ΤΕΛΟΣ_ΑΝ

        return IfNode(condition, body, elif_blocks, else_body)
    
    def parse_var_decl(self):
        self.eat(TokenType.DECLARE)  # ΔΗΛΩΣΕ

        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        # ΩΣ
        if not self.current_token or self.current_token.type != TokenType.AS:
            if errors.CURRENT_EDITION == "EN":
                message = "Expected keyword 'AS'"
            else:
                message = "Αναμενόταν η λέξη-κλειδί 'ΩΣ'"

            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                message
            )
        self.eat(TokenType.AS)

        # Τύπος
        var_type = self.current_token.type
        self.advance()

        # =
        self.eat(TokenType.ASSIGN)

        # expression
        expr_parser = ExpressionParser(self.tokens[self.pos:])
        value = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        return VarDeclNode(name, var_type, value)
    
    def parse_block(self):

        statements = []

        while True:
            # αν τελείωσε το block → σταμάτα
            if (
                self.current_token.type in (
                    TokenType.ELSE_IF,
                    TokenType.ELSE,
                    TokenType.END_IF,
                    TokenType.END_FOR,
                    TokenType.END_WHILE,
                    TokenType.END_FUNCTION
                )
            ):
                break

            stmt = self.parse()
            if stmt is None:
                break

            statements.append(stmt)

        return statements
    
    def parse_for(self):

        self.eat(TokenType.FOR)  # ΓΙΑ

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        # --- CORE 1.4: FOR EACH ---
        if self.current_token.type == TokenType.IN:
            self.eat(TokenType.IN)

            expr_parser = ExpressionParser(self.tokens[self.pos:])
            collection = expr_parser.parse()

            self.pos += expr_parser.consumed
            self.current_token = self.tokens[self.pos]

            self.eat(TokenType.THEN)
            self.eat(TokenType.COLON)

            body = self.parse_block()

            if not self.current_token or self.current_token.type != TokenType.END_FOR:
                raise ELLISyntaxError(
                    self.current_token.line if self.current_token else -1,
                    "Expected keyword 'END_FOR'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΤΕΛΟΣ_ΓΙΑ'"
                )

            self.eat(TokenType.END_FOR)

            return ForEachNode(var_name, collection, body)

        # ΑΠΟ --- CORE 1.0 ---
        if self.current_token.type != TokenType.FROM:
            raise ELLISyntaxError(
                self.current_token.line,
                "Expected keyword 'FROM'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΑΠΟ'"
            )
        self.eat(TokenType.FROM)

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        start = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        # ΜΕΧΡΙ
        if not self.current_token or self.current_token.type != TokenType.TO:
            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                "Expected keyword 'TO'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΜΕΧΡΙ'"
            )
        self.eat(TokenType.TO)

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        end = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        self.eat(TokenType.COLON)

        body = self.parse_block()

        # εδώ πρέπει να υπάρχει ΤΕΛΟΣ_ΓΙΑ
        if not self.current_token:
            raise ELLISyntaxError(
                -1,
                "End of file before 'END_FOR'" if errors.CURRENT_EDITION == "EN" else "Τέλος αρχείου πριν το 'ΤΕΛΟΣ_ΓΙΑ'"
            )

        if self.current_token.type != TokenType.END_FOR:
            raise ELLISyntaxError(
                self.current_token.line,
                "Expected keyword 'END_FOR'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΤΕΛΟΣ_ΓΙΑ'"
            )
        self.eat(TokenType.END_FOR)

        return ForNode(var_name, start, end, body)
    
    def parse_while(self):

        self.eat(TokenType.WHILE)  # ΟΣΟ

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        condition = expr_parser.parse()

        self.pos += expr_parser.consumed
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        # ΤΟΤΕ
        if not self.current_token or self.current_token.type != TokenType.THEN:
            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                "Expected keyword 'THEN'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΤΟΤΕ'"
            )

        self.eat(TokenType.THEN)
        self.eat(TokenType.COLON)

        body = self.parse_block()

        # ΤΕΛΟΣ_ΟΣΟ
        if not self.current_token or self.current_token.type != TokenType.END_WHILE:
            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                "Expected keyword 'END_WHILE'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΤΕΛΟΣ_ΟΣΟ'"
            )

        self.eat(TokenType.END_WHILE)

        return WhileNode(condition, body)
    
    def parse_function(self):

        self.eat(TokenType.DECLARE)  # ΔΗΛΩΣΕ

        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.AS)  # ΩΣ
        self.eat(TokenType.FUNCTION)  # ΣΥΝΑΡΤΗΣΗ

        self.eat(TokenType.LPAREN)
        self.skip_newlines()

        params = []

        while self.current_token and self.current_token.type != TokenType.RPAREN:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            self.skip_newlines()

            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                self.skip_newlines()

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)

        body = self.parse_block()

        if not self.current_token or self.current_token.type != TokenType.END_FUNCTION:
            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                "Expected keyword 'END_FUNCTION'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ'"
            )
        self.eat(TokenType.END_FUNCTION)  # ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ

        return FuncDefNode(name, params, body)
    
    def parse_function_call(self):

        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.LPAREN)
        self.skip_newlines()

        args = []

        if self.current_token and self.current_token.type != TokenType.RPAREN:

            expr_parser = ExpressionParser(self.tokens[self.pos:])
            arg = expr_parser.parse()

            args.append(arg)
            self.pos += expr_parser.consumed
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            self.skip_newlines()

            while self.current_token and self.current_token.type == TokenType.COMMA:

                self.eat(TokenType.COMMA)
                self.skip_newlines()

                expr_parser = ExpressionParser(self.tokens[self.pos:])
                arg = expr_parser.parse()

                args.append(arg)
                self.pos += expr_parser.consumed
                self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
                self.skip_newlines()

        self.eat(TokenType.RPAREN)

        return FunctionCallNode(name, args)
    
    def parse_list_append(self):

        self.eat(TokenType.LIST_APPEND)  # ΠΡΟΣΘΕΣΕ_ΣΤΗ_ΛΙΣΤΑ
        self.eat(TokenType.LPAREN)
        self.skip_newlines()

        list_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.skip_newlines()

        self.eat(TokenType.COMMA)
        self.skip_newlines()

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        value = expr_parser.parse()

        self.pos += expr_parser.consumed
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        self.skip_newlines()

        self.eat(TokenType.RPAREN)

        return ListAppendNode(list_name, value)
    
    def parse_comment(self):

        self.eat(TokenType.COMMENT)  # ΣΧΟΛΙΟ
        self.eat(TokenType.COLON)

        text = self.current_token.value
        self.eat(TokenType.STRING)

        return CommentNode(text)
    
    def parse_return(self):

        self.eat(TokenType.RETURN)  # ΕΠΙΣΤΡΕΨΕ
        expr_parser = ExpressionParser(self.tokens[self.pos:])
        value = expr_parser.parse()

        self.pos += expr_parser.consumed

        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        return ReturnNode(value)

    def parse_const_decl(self):

        self.eat(TokenType.CONSTANT)

        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        if not self.current_token or self.current_token.type != TokenType.AS:
            raise ELLISyntaxError(
                self.current_token.line if self.current_token else -1,
                "Expected keyword 'AS'" if errors.CURRENT_EDITION == "EN" else "Αναμενόταν η λέξη-κλειδί 'ΩΣ'"
            )

        self.eat(TokenType.AS)

        var_type = self.current_token.type
        self.advance()

        self.eat(TokenType.ASSIGN)

        expr_parser = ExpressionParser(self.tokens[self.pos:])
        value = expr_parser.parse()

        self.pos += expr_parser.consumed

        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

        return ConstDeclNode(name, var_type, value)

    def parse_import(self):
        self.eat(TokenType.IMPORT)

        module_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        return ImportNode(module_name)


    def parse_from_import(self):
        self.eat(TokenType.FROM)

        module_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.IMPORT)

        element_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        return FromImportNode(module_name, element_name)