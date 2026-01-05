from __future__ import annotations

import datetime as dt
import grp
import os
import pwd
import sqlite3
from pathlib import Path

from .config import get_db_path as _get_db_path

SCHEMA_VERSION = 1


def get_db_path() -> str:
    return _get_db_path()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def _schema_meta_exists(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_meta'"
    ).fetchone()
    return row is not None


def _load_schema_sql() -> str:
    schema_path = Path(__file__).with_name("schema.sql")
    return schema_path.read_text(encoding="utf-8")


def _apply_schema(conn: sqlite3.Connection) -> None:
    applied_at = dt.datetime.utcnow().replace(microsecond=0).isoformat()
    applied_at_literal = applied_at.replace("'", "''")
    schema_sql = _load_schema_sql().rstrip()
    schema_with_meta = (
        "BEGIN;\n"
        f"{schema_sql}\n"
        "INSERT INTO schema_meta (version, applied_at)\n"
        f"VALUES ({SCHEMA_VERSION}, '{applied_at_literal}');\n"
        "COMMIT;\n"
    )
    conn.executescript(schema_with_meta)


def _read_schema_version(conn: sqlite3.Connection) -> int | None:
    row = conn.execute("SELECT MAX(version) FROM schema_meta").fetchone()
    if row is None:
        return None
    return row[0]


def init_db() -> None:
    db_path = Path(get_db_path())
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("=== DB DEBUG START ===")
    print("DB PATH:", db_path)

    db_dir = os.path.dirname(db_path)
    print("DB DIR:", db_dir)
    print("DIR EXISTS:", os.path.exists(db_dir))
    print("DIR IS DIR:", os.path.isdir(db_dir))
    print("DIR WRITABLE:", os.access(db_dir, os.W_OK))

    try:
        st = os.stat(db_dir)
        print("DIR MODE:", oct(st.st_mode))
        print(
            "DIR UID:",
            st.st_uid,
            "(",
            pwd.getpwuid(st.st_uid).pw_name
            if st.st_uid in [u.pw_uid for u in pwd.getpwall()]
            else "unknown",
            ")",
        )
        print(
            "DIR GID:",
            st.st_gid,
            "(",
            grp.getgrgid(st.st_gid).gr_name
            if st.st_gid in [g.gr_gid for g in grp.getgrall()]
            else "unknown",
            ")",
        )
    except Exception as e:
        print("STAT ERROR:", e)

    print("PROCESS UID:", os.getuid())
    print("PROCESS GID:", os.getgid())
    print("EUID:", os.geteuid())
    print("EGID:", os.getegid())

    print("=== DB DEBUG END ===")

    with sqlite3.connect(db_path) as conn:
        if not _schema_meta_exists(conn):
            _apply_schema(conn)
            return

        version = _read_schema_version(conn)
        if version is None:
            raise RuntimeError("Corrupt database: schema_meta table is empty.")
        if version != SCHEMA_VERSION:
            raise RuntimeError(
                f"Unsupported schema version: {version}. Expected {SCHEMA_VERSION}."
            )


def get_daily_log(date_value: str) -> dict[str, object] | None:
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT
                date,
                walked,
                no_alcohol_after_21,
                food_respected,
                note,
                special_occasion,
                created_at,
                updated_at
            FROM daily_log
            WHERE date = ?
            """,
            (date_value,),
        ).fetchone()

    if row is None:
        return None

    return {
        "date": row["date"],
        "walked": bool(row["walked"]),
        "no_alcohol_after_21": bool(row["no_alcohol_after_21"]),
        "food_respected": bool(row["food_respected"]),
        "note": row["note"],
        "special_occasion": bool(row["special_occasion"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def upsert_daily_log(
    *,
    date_value: str,
    walked: bool,
    no_alcohol_after_21: bool,
    food_respected: bool,
    note: str | None,
    special_occasion: bool,
) -> None:
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat()

    with _connect() as conn:
        existing = conn.execute(
            "SELECT created_at FROM daily_log WHERE date = ?",
            (date_value,),
        ).fetchone()

        if existing is None:
            conn.execute(
                """
                INSERT INTO daily_log (
                    date,
                    walked,
                    no_alcohol_after_21,
                    food_respected,
                    note,
                    special_occasion,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    date_value,
                    int(walked),
                    int(no_alcohol_after_21),
                    int(food_respected),
                    note,
                    int(special_occasion),
                    now,
                    now,
                ),
            )


def get_weekly_weight(year: int, week: int) -> dict[str, object] | None:
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT
                year,
                week,
                weight_kg,
                created_at
            FROM weekly_weight
            WHERE year = ? AND week = ?
            """,
            (year, week),
        ).fetchone()

    if row is None:
        return None

    return {
        "year": row["year"],
        "week": row["week"],
        "weight_kg": row["weight_kg"],
        "created_at": row["created_at"],
    }


def upsert_weekly_weight(*, year: int, week: int, weight_kg: float) -> None:
    now = dt.datetime.utcnow().replace(microsecond=0).isoformat()

    with _connect() as conn:
        existing = conn.execute(
            "SELECT created_at FROM weekly_weight WHERE year = ? AND week = ?",
            (year, week),
        ).fetchone()

        if existing is None:
            conn.execute(
                """
                INSERT INTO weekly_weight (year, week, weight_kg, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (year, week, weight_kg, now),
            )
        else:
            conn.execute(
                """
                UPDATE weekly_weight
                SET weight_kg = ?
                WHERE year = ? AND week = ?
                """,
                (weight_kg, year, week),
            )
