# DevHub Port Allocation Convention

## Purpose

This document defines a **deterministic port allocation scheme** for all DevHub projects.
The goal is to avoid port collisions, improve readability, and make container-to-project
mapping immediately obvious during operations.

This convention applies to:
- Docker containers
- docker-compose (development only)
- Reverse proxy backends
- Unraid port mappings

---

## Reserved Port Range

**10000 – 19999** is reserved exclusively for **DevHub-managed projects**.

Ports outside this range may be used by:
- system services
- third-party containers
- infrastructure tooling

---

## Port Number Format

```
10PPN
```

Where:
- `PP` = DevHub project number (00–99)
- `N`  = port index within the project (1–9)

This allows:
- up to 100 projects
- up to 9 ports per project

---

## Examples

| Project | Purpose | Port |
|------|--------|------|
| DEVHUB-PROJ-002 | Main application | 10021 |
| DEVHUB-PROJ-002 | Secondary endpoint (future) | 10022 |
| DEVHUB-PROJ-015 | Main application | 10151 |
| DEVHUB-PROJ-099 | Main application | 10991 |

---

## Rules

- Each project **must document** its allocated ports
- Port `N=1` is reserved for the **primary application endpoint**
- Higher `N` values are reserved for future use (admin, metrics, etc.)
- No project may use ports outside its allocated block without explicit justification

---

## Governance

This document defines a **DevHub operational convention**.
It does not affect application architecture and does not require ADRs per project.

Projects must comply unless an explicit exception is documented.
