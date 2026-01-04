# DEVHUB-PROJ-002 — Habit Log

This repository contains the governance baseline for the Habit Log project.

⚠️ Architecture and scope are frozen at v0.
Any changes require an explicit ADR.

See /docs for authoritative documentation.

## Runtime configuration (local development)

This application fails fast if required environment variables are missing.
This is intentional.

### Required variables
- `HABIT_LOG_PASSWORD_HASH`

### Local development setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

Set a password hash value in .env.

Provide the environment variable before starting the app:

```bash
export HABIT_LOG_PASSWORD_HASH=...
python -m src.habit_log
```

The application will not start if required variables are missing.

Runtime configuration
This project uses Docker --env-file.
Any change to .env requires Dev Containers: Rebuild and Reopen.

