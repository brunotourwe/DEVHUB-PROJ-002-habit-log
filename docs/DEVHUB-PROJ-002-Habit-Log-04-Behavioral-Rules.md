# DEVHUB-PROJ-002 — Behavioral Rules (v0)

## Purpose

This document defines **behavioral rules** for the Habit Log application.
These rules describe *how the system interprets time and user interaction*.
They are intentionally separated from architecture and ADRs.

Principle:
> The system favors **honest reflection** over strict enforcement.

---

## 1. Definition of the Default Log Date

The application defines a concept of **behavioral today**.

### Behavioral today

- If the current local time is **before 03:00**,  
  the default log date is **yesterday**.
- If the current local time is **03:00 or later**,  
  the default log date is **today**.

This rule reflects common human behavior where a “day” is not mentally closed at midnight.

---

## 2. Late-Night Logging

- Users are allowed to log the previous day during late-night hours.
- Late-night logging is considered normal behavior, not an exception.
- The system does not warn, block, or flag late-night entries.

---

## 3. Backdating and Forward Navigation

- Users may navigate freely between days.
- Users may create or update logs for **past dates**.
- Users may view future dates, but no assumptions are made about completeness.

Rationale:
> Preventing backdating would encourage dishonesty and reduce trust in the system.

---

## 4. Editing Existing Entries

- Entries for a given date may be edited at any time.
- `created_at` remains unchanged.
- `updated_at` reflects the most recent modification.

No historical revision tracking is implemented in v0.

---

## 5. Non-Goals (Explicit)

The following behaviors are **out of scope for v0**:

- Locking past days
- Enforcing logging deadlines
- Automatic reminders
- Warnings for late or missed logs
- Penalization logic

---

## 6. Governance

- These rules apply to **DEVHUB-PROJ-002 only**.
- Changes require:
  - an explicit update to this document
  - a clear rationale in the commit message
- No ADR is required unless architectural assumptions change.

---

## Status

Behavioral rules are **frozen for v0**.
