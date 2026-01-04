# DEVHUB-PROJ-002 — Habit Log (v0)
## Minimal Stack Proposal

This document translates the approved v0 proposal into a concrete, minimal technology stack and repository layout, aligned with the architecture and ADRs.

---

## 1. Proposed Stack

### Frontend
- Server-rendered HTML templates
- CSS + minimal vanilla JavaScript
- No SPA framework, no build step

### Backend
- Python 3.12
- Flask (WSGI)
- Direct SQL via stdlib `sqlite3`
- Session-based authentication

### Storage
- SQLite database file
- Path provided via environment variable
- Database stored on a single mounted volume

### Container & Deployment
- Single container
- Single volume
- Single service
- HTTP port exposed internally (TLS handled by reverse proxy)

---

## 2. Proposed Repository Structure

```text
projects/DEVHUB-PROJ-002-habit-log/
  .dockerignore
  Dockerfile
  docker-compose.dev.yml
  requirements.txt
  src/
    habit_log/
      __init__.py
      app.py
      auth.py
      db.py
      schema.sql
      templates/
      static/
  docs/
  docs/adr/
```

---

## 3. Required Environment Variables

| Variable | Purpose | Example |
| --- | --- | --- |
| `HABIT_LOG_PASSWORD_HASH` | Hashed password for single-user login | `"..."` |
| `HABIT_LOG_DB_PATH` | SQLite database file path | `/data/habit-log.db` |
| `HABIT_LOG_ENV` | Runtime mode | `production` |
| `HABIT_LOG_HOST` | HTTP bind address | `0.0.0.0` |
| `HABIT_LOG_PORT` | HTTP bind port | `10021` |

Binding requirement:
- The application must bind to `0.0.0.0:10021` inside the container (configurable via `HABIT_LOG_HOST` and `HABIT_LOG_PORT`).

Port allocation note:
- DevHub uses a deterministic port scheme: `10PPN` (PP = project number, N = port index).
- For DEVHUB-PROJ-002, the primary port is `10021`.

Password hash format:
- Use Werkzeug `generate_password_hash` output (default `pbkdf2:sha256` format).
- Generate a hash with:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

---

## 4. Proposed Dockerfile

```Dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/

USER appuser
EXPOSE 10021

CMD ["python", "-m", "habit_log"]
```

---

## 5. Proposed docker-compose.dev.yml (local development only)

```yaml
# Development-only compose file; not for Unraid deployment.
services:
  habit-log:
    build: .
    ports:
      - "10021:10021"
    environment:
      HABIT_LOG_PASSWORD_HASH: "set-me"
      HABIT_LOG_DB_PATH: "/data/habit-log.db"
      HABIT_LOG_ENV: "production"
      HABIT_LOG_HOST: "0.0.0.0"
      HABIT_LOG_PORT: "10021"
    volumes:
      - habit-log-data:/data

volumes:
  habit-log-data:
```

---

## 6. Proposed .dockerignore

```text
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
.env
*.db
*.sqlite
*.sqlite3
```
