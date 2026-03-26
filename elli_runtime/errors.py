CURRENT_EDITION = "EL"

TYPE_NAME_MAP_EN = {
    "ΑΡΙΘΜΟΣ": "NUMBER",
    "ΑΚΕΡΑΙΟΣ": "INTEGER",
    "ΔΕΚΑΔΙΚΟΣ": "DECIMAL",
    "ΚΕΙΜΕΝΟ": "TEXT",
    "ΛΟΓΙΚΟΣ": "BOOLEAN",
    "ΚΕΝΟ": "NULL",
    "ΛΙΣΤΑ": "LIST",
    "ΔΟΜΗ": "STRUCT",
    "ΣΥΝΑΡΤΗΣΗ": "FUNCTION",
    "HTTP_ΑΠΑΝΤΗΣΗ": "HTTP_RESPONSE"
}

def translate_type_name(type_name):
    if CURRENT_EDITION != "EN":
        return type_name

    if not isinstance(type_name, str):
        return type_name

    translated = type_name

    translated = translated.replace(" ή ", " or ")
    translated = translated.replace(" και ", " and ")

    for el_name, en_name in TYPE_NAME_MAP_EN.items():
        translated = translated.replace(el_name, en_name)

    return translated

def set_edition(edition):
    global CURRENT_EDITION
    CURRENT_EDITION = edition

class GreekLangRuntimeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class ELLIError(Exception):
    def __init__(self, error_type, line, message):
        self.error_type = error_type
        self.line = line
        self.message = message
        super().__init__(self.__str__())

    def __str__(self):

        if CURRENT_EDITION == "EN":
            type_map = {
                "ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ": "SYNTAX_ERROR",
                "ΣΦΑΛΜΑ_ΤΥΠΟΥ": "TYPE_ERROR",
                "ΣΦΑΛΜΑ_ΟΝΟΜΑΤΟΣ": "NAME_ERROR",
                "ΣΦΑΛΜΑ_ΜΗΔΕΝΙΚΗΣ_ΔΙΑΙΡΕΣΗΣ": "ZERO_DIVISION_ERROR",
                "ΣΦΑΛΜΑ_ΜΠΛΟΚ": "BLOCK_ERROR",
                "ΣΦΑΛΜΑ_ΕΣΟΧΗΣ": "INDENTATION_ERROR",
                "ΣΦΑΛΜΑ_ΕΙΣΟΔΟΥ_ΕΞΟΔΟΥ": "IO_ERROR",
                "ΣΦΑΛΜΑ_JSON": "JSON_ERROR",
                "ΣΦΑΛΜΑ_ΚΛΕΙΔΙΟΥ": "KEY_ERROR",
                "ΣΦΑΛΜΑ_HTTP": "HTTP_ERROR"
            }

            error_type = type_map.get(self.error_type, self.error_type)
        else:
            error_type = self.error_type

        return f"{error_type} at line {self.line}:\n{self.message}" \
            if CURRENT_EDITION == "EN" \
            else f"{error_type} στη γραμμή {self.line}:\n{self.message}"


class ELLISyntaxError(ELLIError):
    def __init__(self, line, message):
        super().__init__("ΣΦΑΛΜΑ_ΣΥΝΤΑΞΗΣ", line, message)

class ELLINameError(ELLIError):
    def __init__(self, line, name):
        if CURRENT_EDITION == "EN":
            message = f"The variable '{name}' is not declared"
        else:
            message = f"Η μεταβλητή '{name}' δεν έχει δηλωθεί"

        super().__init__(
            "ΣΦΑΛΜΑ_ΟΝΟΜΑΤΟΣ",
            line,
            message
        )

class ELLITypeError(ELLIError):
    def __init__(self, line, expected, given):
        self.expected = expected
        self.given = given
        super().__init__("ΣΦΑΛΜΑ_ΤΥΠΟΥ", line, None)

    def __str__(self):
        expected = self.expected
        given = self.given

        if isinstance(expected, str):
            expected = translate_type_name(expected)

        if isinstance(given, str):
            given = translate_type_name(given)

        if CURRENT_EDITION == "EN":
            return f"TYPE_ERROR at line {self.line}:\nExpected {expected} but got {given}"
        else:
            return f"ΣΦΑΛΜΑ_ΤΥΠΟΥ στη γραμμή {self.line}:\nΑναμενόταν {expected} αλλά δόθηκε {given}"

class ELLIZeroDivisionError(ELLIError):
    def __init__(self, line):
        if CURRENT_EDITION == "EN":
            message = "Division by 0 is not allowed"
        else:
            message = "Δεν επιτρέπεται διαίρεση με το 0"

        super().__init__(
            "ΣΦΑΛΜΑ_ΜΗΔΕΝΙΚΗΣ_ΔΙΑΙΡΕΣΗΣ",
            line,
            message
        )

class ELLIBlockError(ELLIError):
    pass

class ELLIIndentationError(ELLIError):
    pass

class ELLIKeyError(ELLIError):
    def __init__(self, line, key):
        if CURRENT_EDITION == "EN":
            message = f"The key '{key}' does not exist"
        else:
            message = f"Το κλειδί '{key}' δεν υπάρχει"

        super().__init__(
            "ΣΦΑΛΜΑ_ΚΛΕΙΔΙΟΥ",
            line,
            message
        )