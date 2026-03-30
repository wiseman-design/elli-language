# ELLI Programming Language

## Stable Core for Future Systems

---

# What is ELLI?

ELLI is a statically-typed, strictly defined programming language designed with two parallel goals:

1. **Educational clarity** through natural-language syntax  
2. **Architectural discipline** suitable for long-term systems evolution  

ELLI is not a scripting experiment and not a Python clone in Greek.  
It is a language built around consistency, determinism, and explicit structure.

The language is defined through a stable CORE specification:

- **CORE 1.0** – Fundamental syntax, strict type system, execution model  
- **CORE 1.1** – Infrastructure extensions (File, JSON, HTTP)  
- **CORE 1.2** – Structured container type (ΔΟΜΗ / STRUCT)  
- **CORE 1.3** – Module system, CORE/STD architecture separation  

ELLI is designed to grow without losing structural integrity.

---

# Why Strict?

ELLI follows a strict design philosophy:

- Explicit type declarations  
- No implicit type coercion (except controlled text concatenation)  
- No truthy/falsy ambiguity  
- No hidden execution behavior  
- No silent conversions  

Strictness exists for three reasons:

1. **Predictability** – Code behaves exactly as written  
2. **Compiler-readiness** – The language can evolve toward compilation targets  
3. **Systems compatibility** – Deterministic execution is required for serious applications  

ELLI prioritizes clarity over convenience.

---

# Why Bilingual?

ELLI supports multiple keyword vocabularies while preserving a single internal syntax tree (AST).

- EL Edition (Greek keywords)  
- EN Edition (English keywords)  

Both editions:

- Share the same execution engine  
- Share the same type system  
- Produce identical internal structures  

---

## Example (EL)
ΔΗΛΩΣΕ μήνυμα ΩΣ ΚΕΙΜΕΝΟ = "Hello"
ΕΜΦΑΝΙΣΕ: μήνυμα


## Example (EN)
DECLARE message AS TEXT = "Hello"
DISPLAY: message


---

ELLI is not tied to one human language — only to one structural core.

---

# What ELLI Does NOT Do

ELLI intentionally does NOT:

- Provide dynamic typing  
- Perform implicit truth conversions  
- Allow undeclared variables  
- Allow type inference  
- Allow runtime dynamic module loading  
- Introduce hidden object models  
- Change philosophy across minor versions  

ELLI 1.x guarantees backward compatibility within the major version.

---

# Core Philosophy

ELLI is built on five principles:

### 1. Explicitness Over Magic  
Everything must be declared. Everything must be closed. Everything must be typed.

### 2. Deterministic Execution  
No hidden runtime behavior. No silent side effects.

### 3. Stable Architecture  
CORE remains stable. Extensions are modular.

### 4. Modular Growth  
Modules are structured and explicit.  
Public access is controlled through module boundaries.

### 5. Long-Term Discipline  
ELLI is designed to evolve without collapsing under feature pressure.

---

# Architecture Overview

## CORE

The language foundation:

- Type system  
- Control flow  
- Functions  
- ΔΟΜΗ / STRUCT  
- ΛΙΣΤΑ / LIST  
- Error model  
- Module system  

CORE is stable across 1.x versions.

---

## STD (Standard Library)

Implemented as modules on top of CORE:

- File handling  
- JSON  
- HTTP  

STD:

- Uses only CORE mechanisms  
- Does not modify the execution model  
- Does not introduce new type rules  

---

# Module Example

## EL
ΕΙΣΑΓΕ math

ΕΜΦΑΝΙΣΕ: math.PI
ΕΜΦΑΝΙΣΕ: math.ΤΕΤΡΑΓΩΝΟ(4)


## EN
IMPORT math

DISPLAY: math.PI
DISPLAY: math.SQUARE(4)


---

# Versioning Policy

## Language Version

- 1.x → Backward compatible  
- 2.0 → Structural or philosophical changes  

## Modules

Modules may evolve independently without modifying CORE.

---

# Vision

ELLI is not designed to compete through feature count.  
It is designed to compete through structural integrity.

The long-term vision:

- Educational clarity  
- Systems-level compatibility  
- Stable modular expansion  
- Community-driven extensions without core instability  

---

**ELLI Programming Language**  
Stable Core 1.x Series