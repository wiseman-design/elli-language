# ELLI Programming Language

## Complete Language Reference (CORE 1.0 – 1.4)

This document defines the practical usage of the ELLI language based on the stable CORE specification.

Covered versions:

- CORE 1.0 – Syntax, Type System, Execution Model
- CORE 1.1 – File, JSON, HTTP
- CORE 1.2 – ΔΟΜΗ (STRUCT)
- CORE 1.3 – Module System

---

# 1. Program Structure

ELLI uses explicit syntax and strict typing.

## Example (EL)


ΔΗΛΩΣΕ μήνυμα ΩΣ ΚΕΙΜΕΝΟ = "Hello"
ΕΜΦΑΝΙΣΕ: μήνυμα


## Example (EN)


DECLARE message AS TEXT = "Hello"
DISPLAY: message


---

# 2. Type System

ELLI is strictly typed.

## Primitive Types

| EL | EN | Description |
|----|----|-------------|
| ΑΡΙΘΜΟΣ | NUMBER | Numeric value |
| ΑΚΕΡΑΙΟΣ | INTEGER | Integer only |
| ΔΕΚΑΔΙΚΟΣ | DECIMAL | Decimal only |
| ΚΕΙΜΕΝΟ | TEXT | String |
| ΛΟΓΙΚΟΣ | BOOLEAN | ΑΛΗΘΗΣ / ΨΕΥΔΗΣ |
| ΚΕΝΟ | NULL | Absence of value |

---

## Rules

- No implicit conversions  
- No type inference  
- Type mismatch → TypeError  
- Only allowed implicit behavior: TEXT concatenation  

---

# 3. Variable Declaration

## Syntax


ΔΗΛΩΣΕ x ΩΣ ΤΥΠΟΣ = τιμή


## EN


DECLARE x AS TYPE = value


---

## Rules

- Type is mandatory  
- Variable must be declared before use  
- Type cannot change  

---

# 4. Constants (CORE 1.3)

## EL


ΣΤΑΘΕΡΑ PI ΩΣ ΔΕΚΑΔΙΚΟΣ = 3.14159


## EN


CONST PI AS DECIMAL = 3.14159


---

## Rules

- Cannot be reassigned  
- Type must match value  
- Violation → TypeError  

---

# 5. Expressions

## Allowed

- NUMBER with NUMBER  
- TEXT with TEXT  
- TEXT with any type (concatenation)

## Not Allowed

- Mixed numeric and boolean  
- Mixed incompatible types  

---

# 6. Input

## EL


ΔΗΛΩΣΕ όνομα ΩΣ ΚΕΙΜΕΝΟ = ΠΕΣ_ΜΟΥ: "Όνομα;"


## EN


DECLARE name AS TEXT = INPUT: "Name?"


---

## Typed Input

## EL


ΔΗΛΩΣΕ ηλικία ΩΣ ΑΡΙΘΜΟΣ = ΠΕΣ_ΜΟΥ.ΑΡΙΘΜΟΣ: "Ηλικία;"


## EN


DECLARE age AS NUMBER = INPUT.NUMBER: "Age?"


---

## Rules

- Basic input returns TEXT  
- Typed input enforces type  
- Invalid input → TypeError  

---

# 7. Conditions

## EL


ΑΝ x > 10 ΤΟΤΕ:
ΕΜΦΑΝΙΣΕ: "Μεγάλο"
ΑΛΛΙΩΣ:
ΕΜΦΑΝΙΣΕ: "Μικρό"
ΤΕΛΟΣ_ΑΝ


## EN


IF x > 10 THEN:
DISPLAY: "Big"
ELSE:
DISPLAY: "Small"
END_IF


---

## Rules

- Condition must be BOOLEAN  
- No implicit truth evaluation  

---

# 8. Loops

## Numeric Loop (CORE 1.0)

## EL


ΓΙΑ i ΑΠΟ 1 ΜΕΧΡΙ 5:
ΕΜΦΑΝΙΣΕ: i
ΤΕΛΟΣ_ΓΙΑ


## EN


FOR i FROM 1 TO 5:
DISPLAY: i
END_FOR


---

## While Loop

## EL


ΟΣΟ x < 5 ΤΟΤΕ:
x = x + 1
ΤΕΛΟΣ_ΟΣΟ


## EN


WHILE x < 5 THEN:
x = x + 1
END_WHILE


---

# 9. Functions

## EL


ΔΗΛΩΣΕ ΠΡΟΣΘΕΣΕ ΩΣ ΣΥΝΑΡΤΗΣΗ(a, b):
ΕΠΙΣΤΡΕΨΕ a + b
ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ


## EN


DECLARE ADD AS FUNCTION(a, b):
RETURN a + b
END_FUNCTION


---

## Rules

- Must be declared before use  
- May return value or ΚΕΝΟ  
- RETURN terminates function  

---

# 10. Lists

## EL


ΔΗΛΩΣΕ λίστα ΩΣ ΛΙΣΤΑ = [1, 2, 3]


## EN


DECLARE list AS LIST = [1, 2, 3]


---

## Rules

- Indexed access only  
- Nested lists allowed  

---

# 11. ΔΟΜΗ (CORE 1.2)

## EL


ΔΗΛΩΣΕ χρήστης ΩΣ ΔΟΜΗ = {
"όνομα": "Νίκος",
"ηλικία": 25
}


## EN


DECLARE user AS STRUCT = {
"name": "Nick",
"age": 25
}


---

## Rules

- Keys must be TEXT  
- Ordered structure  
- Access via ["key"]  
- No direct comparison  

---

# 12. File (CORE 1.1)

## EL


ΔΗΛΩΣΕ content ΩΣ ΚΕΙΜΕΝΟ = ΑΡΧΕΙΟ.ΑΝΑΓΝΩΣΕ("file.txt")


## EN


DECLARE content AS TEXT = FILE.READ("file.txt")


---

# 13. JSON (CORE 1.1)

## EL


ΔΗΛΩΣΕ data ΩΣ ΔΟΜΗ = JSON.ΑΠΟ_ΚΕΙΜΕΝΟ(text)


## EN


DECLARE data AS STRUCT = JSON.FROM_TEXT(text)


---

## Mapping

- object → STRUCT  
- array → LIST  
- string → TEXT  
- number → NUMBER  
- boolean → BOOLEAN  
- null → NULL  

---

# 14. HTTP (CORE 1.1)

## EL


ΔΗΛΩΣΕ response ΩΣ HTTP_ΑΠΑΝΤΗΣΗ = HTTP.GET(url)


## EN


DECLARE response AS HTTP_RESPONSE = HTTP.GET(url)


---

## Accessors

## EL


HTTP.ΚΩΔΙΚΟΣ(response)
HTTP.ΣΩΜΑ(response)


## EN


HTTP.STATUS(response)
HTTP.BODY(response)


---

# 15. Modules (CORE 1.3)

## Import

## EL


ΕΙΣΑΓΕ math


## EN


IMPORT math


---

## Selective Import

## EL


ΑΠΟ math ΕΙΣΑΓΕ ΤΕΤΡΑΓΩΝΟ


## EN


FROM math IMPORT SQUARE


---

## Rules

- Static loading only  
- No dynamic import  
- Namespace-based access  

---

# 16. Error Model

ELLI produces explicit errors:

- TypeError  
- NameError  
- SyntaxError  
- KeyError  

---

# Final Note

ELLI is strict by design.

It prioritizes:

- clarity  
- determinism  
- structural consistency  

---

# 17. Advanced Iteration (CORE 1.4)

## Collection Loop

## EL

ΓΙΑ x ΣΕ λίστα ΤΟΤΕ:
    ΕΜΦΑΝΙΣΕ: x
ΤΕΛΟΣ_ΓΙΑ


## EN

FOR x IN list THEN:
    DISPLAY: x
END_FOR


## Rules

- Iteration variable is implicitly created
- Variable scope is limited to the loop
- Type is derived from the collection
- Only LIST is supported as iteration source
- No implicit type conversions

---

## Loop Control

## EL

ΔΙΑΚΟΠΗ


## EN

LOOP_BREAK


## Rules

- Terminates nearest loop
- Not allowed outside loop
- Does not affect outer blocks

---

## Math Namespace (CORE 1.4)

Available without import.

## Functions

- ΜΑΘ.ΤΕΤΡΑΓΩΝΟ / MATH.SQUARE
- ΜΑΘ.ΡΙΖΑ / MATH.SQRT
- ΜΑΘ.ΑΠΟΛΥΤΗ / MATH.ABS
- ΜΑΘ.ΕΛΑΧΙΣΤΟ / MATH.MIN
- ΜΑΘ.ΜΕΓΙΣΤΟ / MATH.MAX

## Rules

- Accept only numeric types
- Invalid type → TypeError
- No implicit conversions

**ELLI Programming Language – Reference Guide**