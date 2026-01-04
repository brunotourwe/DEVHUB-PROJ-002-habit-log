from __future__ import annotations

import os
from functools import wraps
from typing import Callable, TypeVar

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

T = TypeVar("T")

SESSION_KEY = "authenticated"


def _get_password_hash() -> str:
    password_hash = os.getenv("HABIT_LOG_PASSWORD_HASH")
    if not password_hash:
        raise RuntimeError("HABIT_LOG_PASSWORD_HASH is required for authentication.")
    return password_hash


def _get_secret_key() -> str:
    secret_key = os.getenv("HABIT_LOG_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("HABIT_LOG_SECRET_KEY is required for sessions.")
    return secret_key


def _is_authenticated() -> bool:
    return bool(session.get(SESSION_KEY))


def login_required(view: Callable[..., T]) -> Callable[..., T]:
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not _is_authenticated():
            return redirect(url_for("login_form", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def register_auth(app: Flask) -> None:
    password_hash = _get_password_hash()
    app.secret_key = _get_secret_key()

    @app.before_request
    def _enforce_auth():
        if request.endpoint in ("health", "login_form", "login_submit", "static"):
            return None
        if not _is_authenticated():
            return redirect(url_for("login_form", next=request.path))
        return None

    @app.get("/login")
    def login_form():
        return render_template(
            "login.html",
            already_authenticated=_is_authenticated(),
            error=None,
            next=request.args.get("next", ""),
        )

    @app.post("/login")
    def login_submit():
        password = request.form.get("password", "")
        next_url = request.form.get("next", "")
        if not next_url.startswith("/"):
            next_url = "/login"

        if check_password_hash(password_hash, password):
            session[SESSION_KEY] = True
            return redirect(next_url)

        return (
            render_template(
                "login.html",
                already_authenticated=False,
                error="Invalid password.",
                next=next_url,
            ),
            401,
        )

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login_form"))
