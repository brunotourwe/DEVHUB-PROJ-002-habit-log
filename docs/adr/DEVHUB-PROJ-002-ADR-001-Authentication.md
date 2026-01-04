# 📄 ADR-001 — Authentication Strategy

**Status:** Accepted  
**Date:** 2026-01-04  
**Project:** DEVHUB-PROJ-002 — Habit Log

---

## Context

The Habit Log application is:
- Single-user
- Personally hosted
- Publicly reachable over the internet
- Not handling sensitive medical or financial data

The authentication mechanism must:
- Prevent casual access
- Remain simple to operate
- Avoid unnecessary identity complexity
- Be robust enough for long-term personal use

---

## Decision

The application will use **simple password-based authentication** with the following characteristics:

- One single user
- Password stored as a hash
- Password provided via environment variable
- Session-based authentication
- No user management, roles, or password reset flows

---

## Rationale

This approach:
- Matches the single-user nature of the application
- Minimizes attack surface
- Avoids dependency on third-party identity providers
- Keeps operational overhead near zero
- Aligns with DevHub’s preference for boring, reliable solutions

---

## Consequences

### Positive
- Very low complexity
- Easy deployment and backup
- No account lifecycle management
- Easy future migration if needed

### Negative
- Not suitable for multi-user scenarios
- Manual password rotation if required

These trade-offs are acceptable for v0.

---

## Alternatives Considered

- Reverse-proxy Basic Auth (rejected: shifts logic outside app)
- OAuth / OpenID (rejected: excessive complexity)
- No authentication (rejected: unacceptable exposure)
