from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_FILENAME = "habit-log.db"
LOCAL_ENVS = {"local", "development", "dev"}


def _get_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


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
    return str(get_data_dir() / DEFAULT_DB_FILENAME)


def get_bind_host() -> str:
    return _get_env("HABIT_LOG_HOST") or "0.0.0.0"


def get_bind_port() -> int:
    return int(_get_env("HABIT_LOG_PORT") or "10021")


def get_password_hash() -> str:
    password_hash = _get_env("HABIT_LOG_PASSWORD_HASH")
    if not password_hash:
        raise RuntimeError("HABIT_LOG_PASSWORD_HASH is required for authentication.")
    return password_hash


def get_secret_key() -> str:
    secret_key = _get_env("HABIT_LOG_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("HABIT_LOG_SECRET_KEY is required for sessions.")
    return secret_key
