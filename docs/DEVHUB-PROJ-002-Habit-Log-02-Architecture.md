# 🏗️ Architecture Overview  
## DEVHUB-PROJ-002 — Habit Log

### 1. Architectural Goals

The architecture is designed to be:

- **Simple** — minimal moving parts  
- **Self-contained** — single deployable unit  
- **Self-hosted** — no cloud dependencies  
- **Honest-by-design** — logic favors visibility over enforcement  
- **Maintainable** — readable, boring, and predictable  

This is a **personal production system**, not a demo.

---

### 2. High-Level System Architecture

```
[ Browser (Mobile / Desktop) ]
            │
            ▼
[ Reverse Proxy (existing Unraid setup) ]
            │
            ▼
[ Habit Log Docker Container ]
   ├── Web UI (responsive)
   ├── Backend API
   ├── Auth layer
   └── Local database (volume-mounted)
```

---

### 3. Deployment Model

- One Docker container  
- One persistent volume  
- One exposed internal HTTP port  
- TLS, DNS, and public exposure handled by existing reverse proxy  

This ensures easy backup, restore, teardown, and operational clarity.

---

### 4. Runtime Components

#### 4.1 Frontend
- Responsive web UI
- Minimal JavaScript
- Focus on speed and clarity
- Calendar-based visual feedback

#### 4.2 Backend
- Authentication
- Daily and weekly logging logic
- Status computation (green/yellow/red)
- Stateless except for database

#### 4.3 Persistence
- Embedded database (SQLite-class)
- Docker volume mounted
- Simple, transparent schema

---

### 5. Authentication Architecture (v0)

- Single-user password-based login
- Password hash via environment variable
- No user management
- No role separation

Security goal:
> Reasonable personal protection, not enterprise-grade security.

---

### 6. Responsive Design (Architectural Requirement)

Responsive design is a **core architectural requirement**.

#### Mobile (Portrait)
- Primary daily usage
- Single-day focus
- Large touch targets
- Sub-30-second interaction

#### Desktop / iPad (Landscape)
- Review and reflection
- Calendar overview
- Weekly and monthly patterns
- Weight history

Single codebase, breakpoint-driven layout, no device detection.

---

### 7. Configuration & Environment

Configured exclusively via environment variables:
- Authentication secret
- Database path
- Runtime mode

No configuration UI.

---

### 8. Operations & Observability

- Docker logs only
- Manual inspection
- Fail-fast behavior

---

### 9. Constraints (Intentional)

- No external APIs
- No background jobs
- No notifications
- No multi-user assumptions

---

### 10. Evolution Path (Non-binding)

Potential future extensions:
- Charts
- Exports
- Multiple users
- Read-only views

Not part of v0.
