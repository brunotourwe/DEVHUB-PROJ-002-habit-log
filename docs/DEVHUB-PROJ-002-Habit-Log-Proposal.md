# 📌 DevHub Project Proposal  
## DEVHUB-PROJ-002 — Habit Log

### 1. Purpose & Motivation

The purpose of this project is to build a **simple, honest, self-hosted web application** that allows the user to log daily health-related habits and weekly weight, with a strong emphasis on **visibility, accountability, and low friction**.

This project is intentionally personal and non-commercial. Its value lies in:
- reinforcing disciplined daily behavior,
- making deviations visible (not hidden),
- and serving as a **realistic, end-to-end DevHub reference project** from design to deployment.

---

### 2. Problem Statement

Existing habit-tracking apps tend to be:
- overly complex,
- overly gamified,
- cloud-dependent,
- or optimized for motivation rather than honesty.

The user explicitly wants a system that:
- does **not prevent** deviation,
- does **not sugar-coat** results,
- but makes “bending the rules” clearly visible over time.

---

### 3. Project Scope — Version 0 (MVP)

#### 3.1 Daily Logging (once per calendar day)

Three boolean questions:
1. Walked sufficiently today? (Yes / No)
2. No alcohol after 21:00? (Yes / No)
3. Food intake respected? (Yes / No)

Optional:
- Free-text note (always allowed)

Daily status rules:
- ✅ All Yes → **Green day**
- ❌ One or more No → **Red day**
- ❌ One No + note marked “special occasion” → **Yellow day**

Constraints (visual only, not enforced):
- Max 2 yellow days per week
- Max 5 yellow days per rolling month

The system **never blocks input**, it only **visualizes outcomes**.

---

#### 3.2 Weekly Logging

- Manual weight input (numeric)
- Frequency: once per week
- No analytics or trends in v0

---

### 4. Non-Goals (Explicitly Out of Scope)

The following are *intentionally excluded* from v0:
- Calorie counting
- Step counters or wearable integrations
- AI coaching or recommendations
- Notifications or reminders
- Multi-user support
- Mobile app
- Data export or reporting
- Charts beyond basic calendar coloring

---

### 5. Target Platform & Deployment

- Runs as a **Docker container**
- Deployed on **Unraid**
- Publicly accessible via existing reverse proxy
- Simple password protection
- Persistent data via mounted volume

The application must be:
- stateless except for its data volume,
- restart-safe,
- backup-friendly.

---

### 6. Authentication & Security (v0)

- Single-user system
- Simple password-based authentication
- Password stored hashed (configured via environment variable)
- No user management

Security goal:  
> “Reasonable personal protection, not enterprise-grade security.”

---

### 7. Data & Persistence

- Lightweight local database (e.g. SQLite)
- One dataset:
  - daily logs
  - weekly weight entries
- No external dependencies

---

### 8. Governance & DevHub Value

This project serves as a **reference implementation** for DevHub practices:
- Clear scope definition
- Versioned delivery (v0 → v1)
- Architecture Decision Records (ADR)
- Docker-first mindset
- Self-hosted production deployment
- Personal ownership from idea to operation

---

### 9. Success Criteria (v0)

The project is considered successful when:
- Daily logging takes < 30 seconds
- The calendar clearly shows green / yellow / red patterns
- Data persists across container restarts
- Deployment on Unraid is documented and repeatable
- The system is used daily for at least one full month

---

### 10. Ownership

- **Product owner:** Bruno Tourwé  
- **Architect:** Bruno Tourwé  
- **Implementation:** Codex (under DevHub rules)  
- **Operations:** Self-hosted (Unraid)
