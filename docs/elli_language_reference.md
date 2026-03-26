# ELLI Programming Language

## Complete Language Reference (CORE 1.0 – 1.3)

This document provides a practical and structured reference for writing code in ELLI.
It covers the language features introduced in:

- CORE 1.0 – Fundamental Syntax & Type System
- CORE 1.1 – File, JSON, HTTP
- CORE 1.2 – ΔΟΜΗ (Structured Container)
- CORE 1.3 – Modules, Visibility, Architecture

This guide is written to allow a new user to start writing ELLI code immediately.

---

# 1. Basic Program Structure

ELLI uses explicit block termination and strict typing.

Example:

```
ΔΗΛΩΣΕ μήνυμα ΩΣ ΚΕΙΜΕΝΟ = "Hello"
ΕΜΦΑΝΙΣΕ: μήνυμα
```

All variables must be declared with a type.

---

# 2. Built-in Types

## Primitive Types

| Type (EL) | Type (EN) | Description |
|------------|------------|-------------|
| ΑΡΙΘΜΟΣ | NUMBER | Integer numeric value |
| ΔΕΚΑΔΙΚΟΣ | DECIMAL | Floating-point value |
| ΚΕΙΜΕΝΟ | TEXT | String value |
| ΛΟΓΙΚΟΣ | BOOLEAN | ΑΛΗΘΗΣ / ΨΕΥΔΗΣ |
| ΚΕΝΟ | NULL | Absence of value |

ELLI is strictly typed:

- No implicit conversions
- No truthy/falsy coercion
- Type mismatch → TypeError

---

# 3. Variable Declaration

```
ΔΗΛΩΣΕ x ΩΣ ΑΡΙΘΜΟΣ = 10
```

Declaration without explicit type is not allowed.

---

# 4. Constants (CORE 1.3)

```
ΣΤΑΘΕΡΑ PI ΩΣ ΔΕΚΑΔΙΚΟΣ = 3.14159
```

Rules:

- Must declare type
- Cannot be reassigned
- Violations → TypeError

---

# 5. Control Flow

## If Condition

```
ΑΝ x > 5 ΤΟΤΕ:
    ΕΜΦΑΝΙΣΕ: "Μεγαλύτερο"
ΤΕΛΟΣ_ΑΝ
```

## Loop

```
ΓΙΑ i ΑΠΟ 0 ΜΕΧΡΙ 10:
    ΕΜΦΑΝΙΣΕ: i
ΤΕΛΟΣ_ΓΙΑ
```

Blocks must close explicitly.

---

# 6. Functions

```
ΔΗΜΟΣΙΟ ΣΥΝΑΡΤΗΣΗ ΤΕΤΡΑΓΩΝΟ(x):
    ΕΠΙΣΤΡΕΨΕ x * x
ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ
```

Functions:

- May be public or private (inside modules)
- Follow strict return behavior

---

# 7. Lists (CORE 1.0 / 1.1)

```
ΔΗΛΩΣΕ λίστα ΩΣ ΛΙΣΤΑ = [1, 2, 3]
```

Nested lists allowed:

```
[[1,2],[3,4]]
```

Access via index:

```
λίστα[0]
```

---

# 8. ΔΟΜΗ (CORE 1.2)

Structured key–value container.

```
ΔΗΛΩΣΕ χρήστης ΩΣ ΔΟΜΗ = {
    "όνομα": "Νίκος",
    "ηλικία": 25
}
```

Access:

```
χρήστης["όνομα"]
```

Rules:

- Keys must be TEXT
- Values may be primitive, LIST, or ΔΟΜΗ
- No implicit conversions
- No direct structure comparison

---

# 9. File Handling (CORE 1.1)

```
ΔΗΛΩΣΕ περιεχόμενο ΩΣ ΚΕΙΜΕΝΟ = ΑΡΧΕΙΟ.ΑΝΑΓΝΩΣΕ("data.txt")
ΑΡΧΕΙΟ.ΓΡΑΨΕ("data.txt", "example")
```

---

# 10. JSON (CORE 1.1)

```
ΔΗΛΩΣΕ δεδομένα ΩΣ ΔΟΜΗ = JSON.ΑΠΟ_ΚΕΙΜΕΝΟ(text)
ΔΗΛΩΣΕ json ΩΣ ΚΕΙΜΕΝΟ = JSON.ΣΕ_ΚΕΙΜΕΝΟ(δεδομένα)
```

JSON maps to:

- object → ΔΟΜΗ
- array → ΛΙΣΤΑ
- string → ΚΕΙΜΕΝΟ
- number → ΑΡΙΘΜΟΣ
- boolean → ΛΟΓΙΚΟΣ
- null → ΚΕΝΟ

---

# 11. HTTP (CORE 1.1)

Blocking model.

```
ΔΗΛΩΣΕ απάντηση ΩΣ HTTP_ΑΠΑΝΤΗΣΗ = HTTP.GET("https://example.com")
ΔΗΛΩΣΕ κωδικός ΩΣ ΑΡΙΘΜΟΣ = HTTP.ΚΩΔΙΚΟΣ(απάντηση)
```

---

# 12. Modules (CORE 1.3)

## Import

```
ΕΙΣΑΓΕ math
```

## Selective Import

```
ΑΠΟ math ΕΙΣΑΓΕ ΤΕΤΡΑΓΩΝΟ
```

## Visibility

- ΔΗΜΟΣΙΟ → exported
- ΙΔΙΩΤΙΚΟ → internal
- Default = private

Modules reside in:

```
modules/
```

Nested modules allowed.

No dynamic loading.
No absolute path imports.

---

# 13. Error Model

ELLI produces explicit errors:

- TypeError
- NameError
- KeyError
- ModuleError
- SyntaxError

No silent failure.

---

# 14. Language Guarantees

ELLI 1.x guarantees:

- Stable syntax
- Strict typing
- Deterministic execution
- Modular structure
- Backward compatibility

---

# 15. English Edition

All keywords may exist in English form while preserving the same grammar and AST.

Example (EN Edition):

```
DECLARE message AS TEXT = "Hello"
PRINT: message
```

Both EL and EN editions behave identically.

---

# Final Note

ELLI is strict by design.
It favors clarity, determinism, and structural integrity over convenience.

This reference is intended as a stable foundation for Version 1.x.

**ELLI Programming Language – Complete Language Reference**

