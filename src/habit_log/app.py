from __future__ import annotations

import os
import sqlite3
from datetime import date as dt_date
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from .auth import login_required, register_auth
from .db import get_daily_log, get_db_path, init_db, upsert_daily_log


def _get_bind() -> tuple[str, int]:
    host = os.getenv("HABIT_LOG_HOST", "0.0.0.0")
    port = int(os.getenv("HABIT_LOG_PORT", "10021"))
    return host, port


def create_app() -> Flask:
    init_db()

    app = Flask(__name__)
    register_auth(app)

    def _check_db_readonly() -> None:
        db_path = Path(get_db_path())
        db_uri = f"file:{db_path.as_posix()}?mode=ro"
        with sqlite3.connect(db_uri, uri=True) as conn:
            conn.execute("SELECT 1").fetchone()

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        try:
            _check_db_readonly()
        except sqlite3.Error:
            return {"status": "error"}, 500
        return {"status": "ok"}, 200

    @app.route("/", methods=["GET", "POST"])
    @login_required
    def daily_log():
        error = None
        if request.method == "POST":
            date_value = request.form.get("date", "")
            try:
                dt_date.fromisoformat(date_value)
            except ValueError:
                error = "Invalid date."
            else:
                walked = request.form.get("walked") == "on"
                no_alcohol_after_21 = request.form.get("no_alcohol_after_21") == "on"
                food_respected = request.form.get("food_respected") == "on"
                special_occasion = request.form.get("special_occasion") == "on"
                note = request.form.get("note", "").strip() or None

                upsert_daily_log(
                    date_value=date_value,
                    walked=walked,
                    no_alcohol_after_21=no_alcohol_after_21,
                    food_respected=food_respected,
                    note=note,
                    special_occasion=special_occasion,
                )
                return redirect(url_for("daily_log", date=date_value))

        date_value = request.args.get("date")
        if not date_value:
            date_value = dt_date.today().isoformat()
        else:
            try:
                dt_date.fromisoformat(date_value)
            except ValueError:
                error = "Invalid date."
                date_value = dt_date.today().isoformat()

        entry = get_daily_log(date_value)

        return render_template(
            "daily_log.html",
            date_value=date_value,
            entry=entry,
            error=error,
        )

    return app


def run() -> None:
    host, port = _get_bind()
    app = create_app()
    app.run(host=host, port=port)
