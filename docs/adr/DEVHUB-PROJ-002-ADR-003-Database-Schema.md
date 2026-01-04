# 📄 ADR-003 — Database Schema (v0)

**Status:** Accepted  
**Date:** 2026-01-04  
**Project:** DEVHUB-PROJ-002 — Habit Log

---

## 1. Context

The Habit Log application stores:
- daily habit evaluations
- optional daily notes
- weekly weight entries

Constraints:
- single user
- low write frequency
- no concurrency concerns
- local embedded database
- schema must be readable and explainable without ORM magic

---

## 2. Design Principles

The schema must be:
- **Explicit** — no derived data stored
- **Time-based** — calendar is the core mental model
- **Immutable per day** — one record per day max
- **Honest** — flags reflect input, not inferred logic

---

## 3. Tables Overview

| Table | Purpose |
|------|---------|
| daily_log | One row per calendar day |
| weekly_weight | One row per ISO week |
| schema_meta | Schema versioning |

---

## 4. Table Definitions

### 4.1 daily_log

```sql
daily_log
---------
date                DATE        PRIMARY KEY
walked              BOOLEAN     NOT NULL
no_alcohol_after_21 BOOLEAN     NOT NULL
food_respected      BOOLEAN     NOT NULL

note                TEXT        NULL
special_occasion    BOOLEAN     NOT NULL DEFAULT FALSE

created_at          TIMESTAMP   NOT NULL
updated_at          TIMESTAMP   NOT NULL
```

Rules:
- `date` is unique
- `special_occasion` is user-declared
- Day status is computed in application code

---

### 4.2 weekly_weight

```sql
weekly_weight
-------------
year                INTEGER     NOT NULL
week                INTEGER     NOT NULL
weight_kg           REAL        NOT NULL

created_at          TIMESTAMP   NOT NULL

PRIMARY KEY (year, week)
```

---

### 4.3 schema_meta

```sql
schema_meta
-----------
version             INTEGER     PRIMARY KEY
applied_at          TIMESTAMP   NOT NULL
```

Initial version: `1`

---

## 5. Explicit Non-Storage Decisions

The following are not stored:
- day status (green/yellow/red)
- counters or aggregates
- compliance percentages

Derived data remains derivable.

---

## 6. Migration Strategy (v0)

- Schema created on first startup
- No auto-migrations
- Future changes require a new ADR

---

## 7. Consequences

### Positive
- Clear and minimal model
- Easy backup & restore
- Human-readable

### Negative
- More logic in application layer
- No edit history

---

## 8. Schema State

Schema is **locked** for v0.
