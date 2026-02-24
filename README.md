# Habit Log

Habit Log is a small Flask app for daily behavior tracking and weekly weight capture.

Project goals:
- easy local testing from this folder,
- GitHub as backup/source of truth,
- deployable as a container on Unraid.

## Local Run (Python)

```bash
./scripts/setup-local
source .venv/bin/activate
./scripts/dev
```

App URL: `http://127.0.0.1:10021`

In local mode (`APP_ENV=local`), if `HABIT_LOG_PASSWORD_HASH` is not set, the default login password is `test123`.

## Local Run (Docker Compose)

```bash
docker compose up --build
```

App URL: `http://127.0.0.1:10021`

Persistent data is stored in `./.data`.

## GitHub Sync Workflow

```bash
git pull --rebase origin main
git add -A
git commit -m "your message"
git push origin main
```

## Deploy On Unraid

Image:
`ghcr.io/brunotourwe/devhub-proj-002-habit-log:latest`

Use production configuration:
- `APP_ENV=production`
- `HABIT_LOG_PASSWORD_HASH` (required)
- `HABIT_LOG_SECRET_KEY` (required)
- map a persistent host folder to `/app/data`
- expose port `10021`

Example:
```bash
docker run -d --name habit-log \
  --restart unless-stopped \
  -p 10021:10021 \
  -e APP_ENV=production \
  -e HABIT_LOG_PASSWORD_HASH='...' \
  -e HABIT_LOG_SECRET_KEY='...' \
  -v /mnt/user/appdata/habit-log:/app/data:rw \
  ghcr.io/brunotourwe/devhub-proj-002-habit-log:latest
```

## Generate Password Hash

```bash
.venv/bin/python - <<'PY'
from werkzeug.security import generate_password_hash
print(generate_password_hash("your-password"))
PY
```
