from __future__ import annotations

import os
from pathlib import Path

from werkzeug.security import generate_password_hash

DEFAULT_DB_FILENAME = "habit-log.db"
LOCAL_ENVS = {"local", "development", "dev"}
DEFAULT_SESSION_DAYS = 30
DEFAULT_LOCAL_PASSWORD = "test123"
DEFAULT_LOCAL_SECRET_KEY = "dev-secret-key-change-me"


def _get_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _get_env_bool(name: str) -> bool | None:
    value = _get_env(name)
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes", "on"}


def get_app_env() -> str:
    return _get_env("APP_ENV") or _get_env("HABIT_LOG_ENV") or "local"


def is_local_env() -> bool:
    return get_app_env().lower() in LOCAL_ENVS


def get_data_dir() -> Path:
    data_dir = _get_env("DATA_DIR") or _get_env("HABIT_LOG_DATA_DIR")
    if data_dir:
        return Path(data_dir)
    if is_local_env():
        return Path.cwd() / ".data"
    raise RuntimeError("DATA_DIR is required when APP_ENV is not local.")


def get_db_path() -> str:
    db_path = _get_env("HABIT_LOG_DB_PATH")
    if db_path:
        return db_path
    data_dir_path = get_data_dir()
    return str(data_dir_path / DEFAULT_DB_FILENAME)


def get_bind_host() -> str:
    return _get_env("HABIT_LOG_HOST") or "0.0.0.0"


def get_bind_port() -> int:
    return int(_get_env("HABIT_LOG_PORT") or "10021")


def get_password_hash() -> str:
    password_hash = _get_env("HABIT_LOG_PASSWORD_HASH")
    if password_hash:
        return password_hash
    if is_local_env():
        return generate_password_hash(DEFAULT_LOCAL_PASSWORD)
    raise RuntimeError("HABIT_LOG_PASSWORD_HASH is required for authentication.")


def get_secret_key() -> str:
    secret_key = _get_env("HABIT_LOG_SECRET_KEY")
    if secret_key:
        return secret_key
    if is_local_env():
        return DEFAULT_LOCAL_SECRET_KEY
    raise RuntimeError("HABIT_LOG_SECRET_KEY is required for sessions.")


def get_session_days() -> int:
    session_days = _get_env("HABIT_LOG_SESSION_DAYS")
    if session_days is None:
        return DEFAULT_SESSION_DAYS
    return int(session_days)


def get_session_cookie_secure() -> bool:
    secure = _get_env_bool("HABIT_LOG_SESSION_COOKIE_SECURE")
    if secure is None:
        return False
    return secure
