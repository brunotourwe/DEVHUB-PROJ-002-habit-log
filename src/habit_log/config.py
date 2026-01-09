from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_FILENAME = "habit-log.db"
LOCAL_ENVS = {"local", "development", "dev"}
_CONFIG_DEBUG_LOGGED = False
DEFAULT_SESSION_DAYS = 30


def _log_config(app_env: str, data_dir: str | None, db_path: str) -> None:
    global _CONFIG_DEBUG_LOGGED
    if _CONFIG_DEBUG_LOGGED:
        return
    _CONFIG_DEBUG_LOGGED = True
    print("CONFIG DEBUG:")
    print("APP_ENV:", app_env)
    print("DATA_DIR:", data_dir)
    print("DB_PATH:", db_path)


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
    app_env = get_app_env()
    db_path = _get_env("HABIT_LOG_DB_PATH")
    if db_path:
        data_dir = _get_env("DATA_DIR") or _get_env("HABIT_LOG_DATA_DIR")
        if not data_dir and app_env.lower() in LOCAL_ENVS:
            data_dir = str(Path.cwd() / ".data")
        _log_config(app_env, data_dir, db_path)
        return db_path
    data_dir_path = get_data_dir()
    db_path = str(data_dir_path / DEFAULT_DB_FILENAME)
    _log_config(app_env, str(data_dir_path), db_path)
    return db_path


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
