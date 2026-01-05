from __future__ import annotations

import sqlite3
from datetime import date as dt_date, timedelta
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from .auth import login_required, register_auth
from .config import get_bind_host, get_bind_port
from .db import (
    get_daily_log,
    get_db_path,
    get_weekly_weight,
    init_db,
    upsert_daily_log,
    upsert_weekly_weight,
)


def _get_bind() -> tuple[str, int]:
    return get_bind_host(), get_bind_port()


def _compute_day_status(
    *,
    walked: bool,
    food_respected: bool,
    no_alcohol_after_21: bool,
) -> str:
    if walked and food_respected and no_alcohol_after_21:
        return "green"
    return "red"


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
        today_value = dt_date.today().isoformat()

        if request.method == "POST":
            error = None
            date_value = request.form.get("date", "")

            try:
                dt_date.fromisoformat(date_value)
            except ValueError:
                error = "Invalid date."
                date_value = today_value

            current = dt_date.today().isocalendar()
            week_year = current.year
            week_number = current.week
            weekly_entry = get_weekly_weight(week_year, week_number)
            edit_weight = request.form.get("edit_weight") == "1"

            if error is None:
                allow_weight_edit = weekly_entry is None or edit_weight
                weight_value = request.form.get("weight_kg", "").strip()

                if weight_value and allow_weight_edit:
                    try:
                        weight_kg = float(weight_value)
                    except ValueError:
                        error = "Weight must be a number."
                    else:
                        upsert_weekly_weight(
                            year=week_year,
                            week=week_number,
                            weight_kg=weight_kg,
                        )

            if error is None:
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

            params: dict[str, str] = {"date": date_value}
            if edit_weight:
                params["edit_weight"] = "1"
            if error:
                params["error"] = error
            return redirect(url_for("daily_log", **params))

        error = request.args.get("error")
        date_value = request.args.get("date") or today_value

        try:
            dt_date.fromisoformat(date_value)
        except ValueError:
            error = "Invalid date."
            date_value = today_value

        current = dt_date.today().isocalendar()
        week_year = current.year
        week_number = current.week
        weekly_entry = get_weekly_weight(week_year, week_number)
        entry = get_daily_log(date_value)

        if entry is None:
            walked = False
            no_alcohol_after_21 = False
            food_respected = False
            special_occasion = False
            note = ""
        else:
            walked = entry["walked"]
            no_alcohol_after_21 = entry["no_alcohol_after_21"]
            food_respected = entry["food_respected"]
            special_occasion = entry["special_occasion"]
            note = entry["note"] or ""

        day_status = _compute_day_status(
            walked=walked,
            food_respected=food_respected,
            no_alcohol_after_21=no_alcohol_after_21,
        )

        recent_days = []
        for offset in range(7):
            day = dt_date.today() - timedelta(days=offset)
            day_value = day.isoformat()
            day_entry = get_daily_log(day_value)
            if day_entry is None:
                day_walked = False
                day_no_alcohol_after_21 = False
                day_food_respected = False
            else:
                day_walked = day_entry["walked"]
                day_no_alcohol_after_21 = day_entry["no_alcohol_after_21"]
                day_food_respected = day_entry["food_respected"]
            recent_days.append(
                {
                    "date": day_value,
                    "status": _compute_day_status(
                        walked=day_walked,
                        food_respected=day_food_respected,
                        no_alcohol_after_21=day_no_alcohol_after_21,
                    ),
                }
            )

        edit_weight = request.args.get("edit_weight") == "1"
        weekly_editable = weekly_entry is None or edit_weight

        return render_template(
            "daily_log.html",
            date_value=date_value,
            entry=entry,
            error=error,
            walked=walked,
            no_alcohol_after_21=no_alcohol_after_21,
            food_respected=food_respected,
            special_occasion=special_occasion,
            note=note,
            day_status=day_status,
            recent_days=recent_days,
            weekly_entry=weekly_entry,
            weekly_editable=weekly_editable,
            weekly_label=f"{week_year}-W{week_number:02d}",
        )

# Legacy / fallback route.
# Primary UX for weekly weight is integrated into the daily log ("/").

    @app.route("/weight", methods=["GET", "POST"])
    @login_required
    def weekly_weight():
        error = None
        current = dt_date.today().isocalendar()
        current_year = current.year
        current_week = current.week

        if request.method == "POST":
            weight_value = request.form.get("weight_kg", "").strip()
            if not weight_value:
                error = "Weight is required."
            else:
                try:
                    weight_kg = float(weight_value)
                except ValueError:
                    error = "Weight must be a number."
                else:
                    upsert_weekly_weight(
                        year=current_year,
                        week=current_week,
                        weight_kg=weight_kg,
                    )
                    return redirect(url_for("weekly_weight"))

        entry = get_weekly_weight(current_year, current_week)

        return render_template(
            "weekly_weight.html",
            entry=entry,
            error=error,
            year=current_year,
            week=current_week,
        )

    return app


def run() -> None:
    host, port = _get_bind()
    app = create_app()
    app.run(host=host, port=port)
