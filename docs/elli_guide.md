# ELLI Programming Language

## Installation, Usage & Contribution Guide

---

# Installation

ELLI is currently distributed as a language specification and reference implementation.

## Requirements

- Supported operating system
- ELLI interpreter or compiler (depending on distribution)
- Project directory structure

## Basic Setup

1. Install the ELLI runtime.
2. Create a project directory.
3. Add a main source file:

```
main.elli
```

4. (Optional) Create a modules directory for modular projects:

```
modules/
```

---

# Getting Started

A minimal ELLI program:

```
ΔΗΛΩΣΕ μήνυμα ΩΣ ΚΕΙΜΕΝΟ = "Hello, ELLI"
ΕΜΦΑΝΙΣΕ: μήνυμα
```

Run using the ELLI runtime:

```
elli main.elli
```

ELLI requires explicit type declarations and strict structure.

---

# Example Program (Modular)

## Project Structure

```
project/
│
├── main.elli
└── modules/
    └── math.elli
```

## modules/math.elli

```
ΔΗΜΟΣΙΟ ΣΤΑΘΕΡΑ PI ΩΣ ΔΕΚΑΔΙΚΟΣ = 3.14159

ΔΗΜΟΣΙΟ ΣΥΝΑΡΤΗΣΗ ΤΕΤΡΑΓΩΝΟ(x):
    ΕΠΙΣΤΡΕΨΕ x * x
ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗ
```

## main.elli

```
ΕΙΣΑΓΕ math

ΕΜΦΑΝΙΣΕ: math.PI
ΕΜΦΑΝΙΣΕ: math.ΤΕΤΡΑΓΩΝΟ(4)
```

---

# Project Structure Guidelines

Recommended layout for scalable applications:

```
project/
│
├── main.elli
├── modules/
│   ├── core/
│   ├── ai/
│   └── utils/
└── tests/
```

Rules:

- All reusable components belong in `modules/`
- Avoid circular dependencies
- Use visibility modifiers (ΔΗΜΟΣΙΟ / ΙΔΙΩΤΙΚΟ)
- Keep public APIs minimal and intentional

---

# Contributing

ELLI is designed for disciplined growth.

## Contribution Principles

1. Do not modify CORE philosophy lightly.
2. Maintain backward compatibility within 1.x.
3. Avoid implicit behavior proposals.
4. Prefer modular extensions over core changes.

## Submitting Proposals

Proposals should include:

- Motivation
- Architectural impact analysis
- Backward compatibility assessment
- Example usage

Core-breaking proposals are considered for 2.0.

---

# Roadmap (High-Level)

## Short-Term

- Stabilize CORE 1.x
- Improve tooling
- Expand documentation

## Mid-Term

- Formal module manifest system
- Dependency resolution model
- Standardized library packaging

## Long-Term

- Optional compilation targets
- Performance optimization layer
- Systems-level integration capabilities

---

# Design Guarantees

ELLI 1.x guarantees:

- Stable syntax
- Stable type system
- Deterministic execution model
- Explicit modular boundaries
- Backward compatibility across minor versions

ELLI does not guarantee:

- Feature expansion without architectural review
- Dynamic typing support
- Implicit runtime flexibility

---

**ELLI Programming Language**  
Usage & Ecosystem Guide

