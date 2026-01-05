# DEVHUB-PROJ-002 — Habit Log

This repository contains the governance baseline for the Habit Log project.

⚠️ Architecture and scope are frozen at v0.
Any changes require an explicit ADR.

See /docs for authoritative documentation.

Data persistence

The application stores its database in a Docker volume / mapped directory.
Rebuilding or upgrading the container does not delete existing data.
To reset data, explicitly remove the volume or mapped folder.

## Running in Unraid / Docker

Image: `ghcr.io/brunotourwe/devhub-proj-002-habit-log:latest`

Required environment variables:
- `HABIT_LOG_PASSWORD_HASH`
- `HABIT_LOG_SECRET_KEY`

Optional environment variables (defaults shown):
- `APP_ENV=production`
- `DATA_DIR=/app/data`
- `HABIT_LOG_HOST=0.0.0.0`
- `HABIT_LOG_PORT=10021`
- `HABIT_LOG_DB_PATH=/app/data/habit-log.db`

Expose port `10021` and mount `/app/data` for persistence.

Example:
```bash
docker run -d --name habit-log \
  -p 10021:10021 \
  -e HABIT_LOG_PASSWORD_HASH=... \
  -e HABIT_LOG_SECRET_KEY=... \
  -v /path/on/host:/app/data \
  ghcr.io/brunotourwe/devhub-proj-002-habit-log:latest
```

## Runtime configuration (local development)

This application fails fast if required environment variables are missing.
This is intentional.

### Required variables
- `HABIT_LOG_PASSWORD_HASH`
- `HABIT_LOG_SECRET_KEY`

### Local development setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

Set a password hash value in .env.

Provide the environment variable before starting the app:

```bash
export HABIT_LOG_PASSWORD_HASH=...
export HABIT_LOG_SECRET_KEY=...
python -m src.habit_log
```

The application will not start if required variables are missing.

Runtime configuration
This project uses Docker --env-file.
Any change to .env requires Dev Containers: Rebuild and Reopen.
