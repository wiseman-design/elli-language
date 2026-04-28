from enum import Enum, auto


class TokenType(Enum):

    # identifiers
    IDENTIFIER = auto()

    # values
    NUMBER = auto()
    STRING = auto()

    # operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    ASSIGN = auto()

    # comparison
    EQ = auto()
    NE = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()

    # symbols
    LPAREN = auto()
    RPAREN = auto()

    LBRACKET = auto()
    RBRACKET = auto()
    DOT = auto()

    COMMA = auto()
    COLON = auto()

    # keywords
    KEYWORD = auto()

    EOF = auto()

    NEWLINE = auto()

    # language semantic tokens
    DECLARE = auto()
    CONSTANT = auto()
    IMPORT = auto()
    FROM = auto()
    AS = auto()

    NUMBER_TYPE = auto()
    INTEGER_TYPE = auto()
    DECIMAL_TYPE = auto()
    TEXT_TYPE = auto()
    LIST_TYPE = auto()
    BOOLEAN_TYPE = auto()
    STRUCT_TYPE = auto()
    HTTP_RESPONSE_TYPE = auto()

    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    DISPLAY = auto()
    INPUT = auto()

    IF = auto()
    THEN = auto()
    ELSE_IF = auto()
    ELSE = auto()
    END_IF = auto()

    FOR = auto()
    IN = auto()
    TO = auto()
    END_FOR = auto()

    WHILE = auto()
    END_WHILE = auto()

    FUNCTION = auto()
    END_FUNCTION = auto()

    RETURN = auto()
    BREAK = auto()
    LOOP_BREAK = auto()
    TERMINATE = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    LIST_APPEND = auto()
    COMMENT = auto()
    TO_BOOLEAN = auto()
    LIST_LENGTH = auto()

    LBRACE = auto()
    RBRACE = auto()