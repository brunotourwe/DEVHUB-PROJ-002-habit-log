from __future__ import annotations

from datetime import timedelta
from functools import wraps
from typing import Callable, TypeVar

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from .config import (
    get_password_hash,
    get_secret_key,
    get_session_cookie_secure,
    get_session_days,
)
T = TypeVar("T")

SESSION_KEY = "authenticated"


def _get_password_hash() -> str:
    return get_password_hash()


def _get_secret_key() -> str:
    return get_secret_key()


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
    app.permanent_session_lifetime = timedelta(days=get_session_days())
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = get_session_cookie_secure()

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
            remember_device=True,
        )

    @app.post("/login")
    def login_submit():
        password = request.form.get("password", "")
        next_url = request.form.get("next", "")
        remember_device = request.form.get("remember_device") == "1"
        if not next_url.startswith("/"):
            next_url = "/login"

        if check_password_hash(password_hash, password):
            session.permanent = remember_device
            session[SESSION_KEY] = True
            return redirect(next_url)

        return (
            render_template(
                "login.html",
                already_authenticated=False,
                error="Invalid password.",
                next=next_url,
                remember_device=remember_device,
            ),
            401,
        )

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login_form"))
