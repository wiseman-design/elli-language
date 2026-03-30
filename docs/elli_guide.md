# ELLI Programming Language

## Installation, Usage & Contribution Guide

---

# Installation

ELLI is distributed as a language specification with a reference runtime.

## Requirements

- Supported operating system
- ELLI runtime (interpreter)
- Project directory

---

## Basic Setup

1. Install the ELLI runtime  
2. Create a project folder  
3. Add a main source file:


main.elli


4. (Optional) Create a modules directory:


modules/


---

# Getting Started

## Minimal Program

### EL


ΔΗΛΩΣΕ μήνυμα ΩΣ ΚΕΙΜΕΝΟ = "Hello, ELLI"
ΕΜΦΑΝΙΣΕ: μήνυμα


### EN


DECLARE message AS TEXT = "Hello, ELLI"
DISPLAY: message


---

## Run Program


elli main.elli


---

# Core Rules

- All variables must be declared with a type  
- No type inference  
- No implicit conversions (except text concatenation)  
- All blocks must close explicitly  
- Conditions must evaluate to BOOLEAN / ΛΟΓΙΚΟΣ  

---

# Project Structure

Recommended layout:


project/
│
├── main.elli
├── modules/
│ └── math.elli
└── tests/


---

# Modular Example

## modules/math.elli

### EL


ΣΤΑΘΕΡΑ PI ΩΣ ΔΕΚΑΔΙΚΟΣ = 3.14159

ΔΗΛΩΣΕ ΤΕΤΡΑΓΩΝΟ ΩΣ ΣΥΝΑΡΤΗΣΗ(x):
ΕΠΙΣΤΡΕΨΕ x * x
ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ


### EN


CONST PI AS DECIMAL = 3.14159

DECLARE SQUARE AS FUNCTION(x):
RETURN x * x
END_FUNCTION


---

## main.elli

### EL


ΕΙΣΑΓΕ math

ΕΜΦΑΝΙΣΕ: math.PI
ΕΜΦΑΝΙΣΕ: math.ΤΕΤΡΑΓΩΝΟ(4)


### EN


IMPORT math

DISPLAY: math.PI
DISPLAY: math.SQUARE(4)


---

# Modules

- Modules are loaded statically before execution  
- Access is performed through namespace (`module.element`)  
- No dynamic import is supported  

---

# JSON Example (CORE 1.1)

### EL


ΔΗΛΩΣΕ δεδομένα ΩΣ ΔΟΜΗ = JSON.ΑΠΟ_ΚΕΙΜΕΝΟ(text)


### EN


DECLARE data AS STRUCT = JSON.FROM_TEXT(text)


---

⚠️ The declared type must match the actual JSON structure.

Mismatch → TypeError

---

# File Example (CORE 1.1)

### EL


ΔΗΛΩΣΕ περιεχόμενο ΩΣ ΚΕΙΜΕΝΟ = ΑΡΧΕΙΟ.ΑΝΑΓΝΩΣΕ("data.txt")


### EN


DECLARE content AS TEXT = FILE.READ("data.txt")


---

# HTTP Example (CORE 1.1)

### EL


ΔΗΛΩΣΕ απάντηση ΩΣ HTTP_ΑΠΑΝΤΗΣΗ = HTTP.GET("https://example.com
")
ΔΗΛΩΣΕ κωδικός ΩΣ ΑΡΙΘΜΟΣ = HTTP.ΚΩΔΙΚΟΣ(απάντηση)


### EN


DECLARE response AS HTTP_RESPONSE = HTTP.GET("https://example.com
")
DECLARE status AS NUMBER = HTTP.STATUS(response)


---

# ΔΟΜΗ Example (CORE 1.2)

### EL


ΔΗΛΩΣΕ χρήστης ΩΣ ΔΟΜΗ = {
"όνομα": "Νίκος",
"ηλικία": 25
}


### EN


DECLARE user AS STRUCT = {
"name": "Nick",
"age": 25
}


---

# Development Guidelines

- Keep logic inside modules  
- Keep main file minimal  
- Avoid circular dependencies  
- Use clear naming  

---

# Contributing

ELLI evolves through structured contributions.

## Principles

1. Respect CORE philosophy  
2. Maintain compatibility  
3. Avoid implicit behavior  
4. Prefer modules over core changes  

---

## Proposal Requirements

- Motivation  
- Design explanation  
- Compatibility analysis  
- Example usage  

---

# Roadmap

## Short-Term

- CORE stabilization  
- Tooling improvements  
- Documentation expansion  

---

## Mid-Term

- Module structuring improvements  
- Dependency handling  

---

## Long-Term

- Compilation targets  
- Performance improvements  

---

# Design Guarantees

ELLI guarantees:

- Deterministic execution  
- Strict typing  
- Explicit syntax  
- Stable CORE  

---

ELLI does NOT support:

- Dynamic typing  
- Implicit conversions  
- Runtime module loading  
- Hidden execution behavior  

---

# Final Note

ELLI is designed for clarity, predictability, and long-term stability.

---

**ELLI Programming Language**  
Usage & Ecosystem Guide