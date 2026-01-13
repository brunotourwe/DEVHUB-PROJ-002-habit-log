from __future__ import annotations

import re
import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import date as dt_date, timedelta
from pathlib import Path
from urllib.parse import unquote

from babel.core import Locale, UnknownLocaleError
from babel.numbers import NumberFormatError, format_decimal, get_decimal_symbol
from flask import Flask, redirect, render_template, request, url_for

from .auth import login_required, register_auth
from .config import get_bind_host, get_bind_port
from .db import (
    count_orange_days,
    get_daily_log,
    get_db_path,
    get_weekly_weight,
    init_db,
    upsert_daily_log,
    upsert_weekly_weight,
)


def _get_bind() -> tuple[str, int]:
    return get_bind_host(), get_bind_port()


DEFAULT_LOCALE = "en_US"
WEIGHT_MIN = Decimal("3")
WEIGHT_MAX = Decimal("500")
WEIGHT_QUANT = Decimal("0.1")
WEIGHT_PATTERN = re.compile(r"^\d+(?:[.,]\d+)?$")


def _normalize_locale(raw_locale: str | None) -> str:
    if not raw_locale:
        return DEFAULT_LOCALE
    value = raw_locale.replace("-", "_")
    try:
        Locale.parse(value)
    except (ValueError, UnknownLocaleError):
        base = value.split("_", 1)[0]
        try:
            Locale.parse(base)
        except (ValueError, UnknownLocaleError):
            return DEFAULT_LOCALE
        return base
    return value


def _decode_cookie(value: str | None) -> str | None:
    if value is None:
        return None
    return unquote(value)


def _get_request_locale() -> str:
    raw_locale = (
        request.form.get("locale")
        or _decode_cookie(request.cookies.get("habit_log_locale"))
        or request.accept_languages.best
    )
    return _normalize_locale(raw_locale)


def _get_request_decimal_symbol(locale: str) -> str:
    symbol = (
        request.form.get("decimal_symbol")
        or _decode_cookie(request.cookies.get("habit_log_decimal"))
        or ""
    ).strip()
    if symbol in {".", ","}:
        return symbol
    return get_decimal_symbol(locale)


def _parse_weight(value: str, decimal_symbol: str) -> Decimal:
    cleaned = value.strip()
    if not cleaned:
        raise NumberFormatError("Empty weight.")
    if not WEIGHT_PATTERN.match(cleaned):
        raise NumberFormatError("Invalid weight format.")

    separator = None
    if "," in cleaned:
        separator = ","
    elif "." in cleaned:
        separator = "."
    if separator and decimal_symbol in {".", ","} and separator != decimal_symbol:
        normalized = cleaned.replace(separator, ".")
    else:
        normalized = cleaned.replace(",", ".")

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise NumberFormatError(str(exc)) from exc


def _normalize_weight(value: Decimal) -> Decimal:
    return value.quantize(WEIGHT_QUANT, rounding=ROUND_HALF_UP)


def _format_weight(value: float | None, locale: str, decimal_symbol: str) -> str:
    if value is None:
        return ""
    try:
        formatted = format_decimal(value, format="0.0", locale=locale)
    except (ValueError, UnknownLocaleError):
        return str(value)
    locale_symbol = get_decimal_symbol(locale)
    if decimal_symbol and decimal_symbol != locale_symbol:
        return formatted.replace(locale_symbol, decimal_symbol)
    return formatted


def _compute_day_status(
    *,
    walked: bool,
    food_respected: bool,
    no_alcohol_after_21: bool,
    special_occasion: bool,
) -> str:
    if walked and food_respected and no_alcohol_after_21:
        return "green"
    if special_occasion:
        return "orange"
    return "red"


def _get_iso_week_bounds(day: dt_date) -> tuple[dt_date, dt_date]:
    week = day.isocalendar()
    start = dt_date.fromisocalendar(week.year, week.week, 1)
    end = dt_date.fromisocalendar(week.year, week.week, 7)
    return start, end


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
        locale = _get_request_locale()
        decimal_symbol = _get_request_decimal_symbol(locale)

        if request.method == "POST":
            error = None
            special_occasion_error = None
            date_value = request.form.get("date", "")
            selected_day = dt_date.today()

            try:
                selected_day = dt_date.fromisoformat(date_value)
            except ValueError:
                error = "Invalid date."
                date_value = today_value
                selected_day = dt_date.fromisoformat(date_value)

            current = selected_day.isocalendar()
            week_year = current.year
            week_number = current.week
            weekly_entry = get_weekly_weight(week_year, week_number)
            edit_weight = request.form.get("edit_weight") == "1"
            allow_weight_edit = weekly_entry is None or edit_weight

            walked = request.form.get("walked") == "on"
            no_alcohol_after_21 = request.form.get("no_alcohol_after_21") == "on"
            food_respected = request.form.get("food_respected") == "on"
            special_occasion = request.form.get("special_occasion") == "on"
            note = request.form.get("note", "").strip() or None
            weight_value = request.form.get("weight_kg", "").strip()
            weight_kg = None

            if error is None and weight_value and allow_weight_edit:
                try:
                    parsed_weight = _parse_weight(weight_value, decimal_symbol)
                    rounded_weight = _normalize_weight(parsed_weight)
                    if rounded_weight < WEIGHT_MIN or rounded_weight > WEIGHT_MAX:
                        raise ValueError("Weight out of range.")
                    weight_kg = float(rounded_weight)
                except (NumberFormatError, ValueError):
                    error = "Weight must be a number between 3.0 and 500.0 kg."

            if error is None:
                day_status = _compute_day_status(
                    walked=walked,
                    food_respected=food_respected,
                    no_alcohol_after_21=no_alcohol_after_21,
                    special_occasion=special_occasion,
                )
                if day_status == "orange":
                    week_start, week_end = _get_iso_week_bounds(selected_day)
                    orange_week = count_orange_days(
                        start_date=week_start.isoformat(),
                        end_date=week_end.isoformat(),
                        exclude_date=date_value,
                    )
                    window_start = selected_day - timedelta(days=29)
                    orange_window = count_orange_days(
                        start_date=window_start.isoformat(),
                        end_date=selected_day.isoformat(),
                        exclude_date=date_value,
                    )
                    if orange_week + 1 > 2:
                        special_occasion_error = (
                            "Only 2 orange days are allowed per ISO week."
                        )
                    elif orange_window + 1 > 5:
                        special_occasion_error = (
                            "Only 5 orange days are allowed in any 30-day window."
                        )

            if error is None and special_occasion_error is None:
                if weight_kg is not None and allow_weight_edit:
                    upsert_weekly_weight(
                        year=week_year,
                        week=week_number,
                        weight_kg=weight_kg,
                    )
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
            if special_occasion_error:
                params["special_occasion_error"] = special_occasion_error
            if error or special_occasion_error:
                params["draft"] = "1"
                params["walked"] = "1" if walked else "0"
                params["no_alcohol_after_21"] = "1" if no_alcohol_after_21 else "0"
                params["food_respected"] = "1" if food_respected else "0"
                params["special_occasion"] = "1" if special_occasion else "0"
            return redirect(url_for("daily_log", **params))

        error = request.args.get("error")
        special_occasion_error = request.args.get("special_occasion_error")
        date_value = request.args.get("date") or today_value

        try:
            selected_day = dt_date.fromisoformat(date_value)
        except ValueError:
            error = "Invalid date."
            date_value = today_value
            selected_day = dt_date.fromisoformat(date_value)

        current = selected_day.isocalendar()
        week_year = current.year
        week_number = current.week
        weekly_entry = get_weekly_weight(week_year, week_number)
        entry = get_daily_log(date_value)
        weekly_weight_display = _format_weight(
            weekly_entry["weight_kg"] if weekly_entry else None,
            locale,
            decimal_symbol,
        )

        use_draft = request.args.get("draft") == "1"
        if use_draft:
            walked = request.args.get("walked") == "1"
            no_alcohol_after_21 = request.args.get("no_alcohol_after_21") == "1"
            food_respected = request.args.get("food_respected") == "1"
            special_occasion = request.args.get("special_occasion") == "1"
            note = entry["note"] if entry and entry["note"] else ""
        elif entry is None:
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
            special_occasion=special_occasion,
        )

        recent_days = []
        for offset in range(1, 8):
            day = selected_day - timedelta(days=offset)
            day_value = day.isoformat()
            day_entry = get_daily_log(day_value)
            if day_entry is None:
                day_walked = False
                day_no_alcohol_after_21 = False
                day_food_respected = False
                day_special_occasion = False
            else:
                day_walked = day_entry["walked"]
                day_no_alcohol_after_21 = day_entry["no_alcohol_after_21"]
                day_food_respected = day_entry["food_respected"]
                day_special_occasion = day_entry["special_occasion"]
            recent_days.append(
                {
                    "date": day_value,
                    "status": _compute_day_status(
                        walked=day_walked,
                        food_respected=day_food_respected,
                        no_alcohol_after_21=day_no_alcohol_after_21,
                        special_occasion=day_special_occasion,
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
            special_occasion_error=special_occasion_error,
            weekly_entry=weekly_entry,
            weekly_editable=weekly_editable,
            weekly_weight_display=weekly_weight_display,
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
        locale = _get_request_locale()
        decimal_symbol = _get_request_decimal_symbol(locale)

        if request.method == "POST":
            weight_value = request.form.get("weight_kg", "").strip()
            if not weight_value:
                error = "Weight is required."
            else:
                try:
                    parsed_weight = _parse_weight(weight_value, decimal_symbol)
                    rounded_weight = _normalize_weight(parsed_weight)
                    if rounded_weight < WEIGHT_MIN or rounded_weight > WEIGHT_MAX:
                        raise ValueError("Weight out of range.")
                    weight_kg = float(rounded_weight)
                except (NumberFormatError, ValueError):
                    error = "Weight must be a number between 3.0 and 500.0 kg."
                else:
                    upsert_weekly_weight(
                        year=current_year,
                        week=current_week,
                        weight_kg=weight_kg,
                    )
                    return redirect(url_for("weekly_weight"))

        entry = get_weekly_weight(current_year, current_week)
        weight_display = _format_weight(
            entry["weight_kg"] if entry else None,
            locale,
            decimal_symbol,
        )

        return render_template(
            "weekly_weight.html",
            entry=entry,
            error=error,
            year=current_year,
            week=current_week,
            weight_display=weight_display,
        )

    return app


def run() -> None:
    host, port = _get_bind()
    app = create_app()
    app.run(host=host, port=port)
