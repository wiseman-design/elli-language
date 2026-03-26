from .tokens import TokenType
import unicodedata
from .errors import ELLIIndentationError, ELLISyntaxError
from elli_runtime import errors

class Token:
    def __init__(self, type_, value, line, indent=0):
        self.type = type_
        self.value = value
        self.line = line
        self.indent = indent

    def __repr__(self):
        return f"{self.type.name}:{self.value} (line {self.line}, indent {self.indent})"


class Lexer:
    def __init__(self, text, keyword_map, forbidden_map):
        self.text = unicodedata.normalize("NFKC", text)
        self.keyword_map = keyword_map
        self.forbidden_map = forbidden_map
        self.pos = 0
        self.line = 1
        self.current_char = self.text[self.pos] if self.text else None

        self.line = 1
        self.at_line_start = True

        self.keyword_map = keyword_map     

    def advance(self):
        if self.current_char == "\n":
            self.line += 1

        self.pos += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        line = self.line

        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        value = float(result) if '.' in result else int(result)
        return Token(TokenType.NUMBER, value, line)

    def identifier(self):
        result = ""
        line = self.line

        while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        # ❌ Ανάμειξη εκδόσεων
        if result in self.forbidden_map:
            if errors.CURRENT_EDITION == "EN":
                message = "Mixing Greek and English keywords is not allowed"
            else:
                message = "Δεν επιτρέπεται ανάμειξη ελληνικών και αγγλικών λέξεων-κλειδιών"

            raise ELLISyntaxError(self.line, message)

        # ✔ Κανονική λέξη-κλειδί
        if result in self.keyword_map:
            return Token(self.keyword_map[result], result, self.line)

        return Token(TokenType.IDENTIFIER, result, self.line)

    def string(self):
        line = self.line
        self.advance()  # skip opening "

        result = ""
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()

        self.advance()  # skip closing "
        return Token(TokenType.STRING, result, line)

    def tokenize(self):
        tokens = []
        token = self.get_next_token()

        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()

        tokens.append(token)
        return tokens

    def get_next_token(self):
        indent = 0
        while self.current_char:

            # NEWLINE
            if self.current_char == '\n':
                self.advance()
                self.at_line_start = True
                return Token(TokenType.NEWLINE, None, self.line - 1)

            # comments
            if self.current_char == '#':
                while self.current_char and self.current_char != '\n':
                    self.advance()
                continue

            # --- ALIGNMENT ONLY ---
            if self.at_line_start:
                indent = 0

                while self.current_char == ' ':
                    indent += 1
                    self.advance()

                # Δεν κάνουμε ΚΑΝΕΝΑ validation εδώ
                # Απλά κρατάμε indent πληροφορία

                self.at_line_start = False

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                token = self.identifier()
                token.indent = indent
                return token

            if self.current_char == '"':
                token = self.string()
                token.indent = indent
                return token

            line = self.line

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, None, line, indent)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, None, line, indent)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, None, line, indent)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, None, line, indent)
            
            if self.current_char == '!':
                line = self.line
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NE, None, line, indent)

                if errors.CURRENT_EDITION == "EN":
                    message = "Unknown operator '!'"
                else:
                    message = "Άγνωστος τελεστής '!'"

                raise ELLISyntaxError(line, message)

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, None, line, indent)
                return Token(TokenType.ASSIGN, None, line, indent)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, None, line, indent)
                return Token(TokenType.GT, None, line, indent)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, None, line, indent)
                return Token(TokenType.LT, None, line, indent)

            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, None, line, indent)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, None, line, indent)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, None, line, indent)

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, None, line, indent)

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, None, line, indent)
            
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, None, line, indent)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, None, line, indent)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, None, line, indent)
            
            if self.current_char == '.':
                line = self.line
                self.advance()
                return Token(TokenType.DOT, None, line, indent)

            if errors.CURRENT_EDITION == "EN":
                message = f"Unknown character '{self.current_char}'"
            else:
                message = f"Άγνωστος χαρακτήρας '{self.current_char}'"

            raise ELLISyntaxError(line, message)

        return Token(TokenType.EOF, None, self.line)