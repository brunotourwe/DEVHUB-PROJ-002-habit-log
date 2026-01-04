# 📄 ADR-002 — Data Storage Strategy

**Status:** Accepted  
**Date:** 2026-01-04  
**Project:** DEVHUB-PROJ-002 — Habit Log

---

## Context

The application requires persistent storage for:
- Daily habit logs
- Weekly weight entries
- Status computation across days and weeks

Requirements:
- Simple
- Reliable
- Backup-friendly
- No external services
- Low operational burden

---

## Decision

The application will use an **embedded relational database** (SQLite-class), with the database file stored on a **Docker-mounted volume**.

---

## Rationale

This approach:
- Requires no separate database service
- Fits the low-concurrency, single-user model
- Is easy to back up and restore
- Keeps the entire system self-contained
- Makes the data human-inspectable if ever needed

---

## Consequences

### Positive
- Extremely low operational complexity
- No networking between services
- High reliability
- Excellent portability

### Negative
- Not suitable for high concurrency
- Limited horizontal scalability

These limitations are irrelevant for the intended use case.

---

## Alternatives Considered

- PostgreSQL / MySQL (rejected: unnecessary operational overhead)
- Cloud database (rejected: violates self-hosting goal)
- Flat files (rejected: schema evolution and integrity risks)
