"""Small supabase auth helper used by the Streamlit frontend.

This module uses the Supabase REST auth endpoints as a lightweight
compatibility layer. It accepts either `SUPABASE_KEY` or
`SUPABASE_ANON_KEY` (preferred for frontends) so it works with both
the assistant-created helpers and user-provided SDK variants.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import httpx


def _get_config() -> tuple[str, str]:
    url = os.getenv("SUPABASE_URL")
    # prefer explicit server key but fall back to anon key for frontend
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY (or SUPABASE_ANON_KEY) environment variables")
    return url.rstrip("/"), key


def _headers(api_key: str) -> Dict[str, str]:
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _extract_user(payload: Dict[str, Any], fallback_email: str = "") -> Dict[str, Any]:
    user = payload.get("user") or payload.get("data", {}).get("user") or {}
    metadata = user.get("user_metadata") or {}
    return {
        "id": user.get("id"),
        "email": user.get("email", fallback_email),
        "name": metadata.get("full_name") or metadata.get("name") or user.get("email", "User"),
        "raw": user,
    }


def login_user(email: str, password: str) -> Dict[str, Any]:
    try:
        url, key = _get_config()
        response = httpx.post(
            f"{url}/auth/v1/token?grant_type=password",
            headers=_headers(key),
            json={"email": email, "password": password},
            timeout=30.0,
        )
        response.raise_for_status()
        return {"success": True, "user": _extract_user(response.json(), email)}
    except Exception as exc:  # pragma: no cover - surfaced in UI
        return {"success": False, "error": str(exc)}


def register_user(email: str, password: str, full_name: str) -> Dict[str, Any]:
    try:
        url, key = _get_config()
        response = httpx.post(
            f"{url}/auth/v1/signup",
            headers=_headers(key),
            json={
                "email": email,
                "password": password,
                "data": {"full_name": full_name, "name": full_name},
            },
            timeout=30.0,
        )
        response.raise_for_status()
        payload = response.json()
        return {
            "success": True,
            "message": payload.get("message", "Account created successfully!"),
            "user": _extract_user(payload, email),
        }
    except Exception as exc:  # pragma: no cover - surfaced in UI
        return {"success": False, "error": str(exc)}


def reset_password(email: str) -> Dict[str, Any]:
    try:
        url, key = _get_config()
        response = httpx.post(
            f"{url}/auth/v1/recover",
            headers=_headers(key),
            json={"email": email},
            timeout=30.0,
        )
        response.raise_for_status()
        return {"success": True, "message": "If that email exists, a reset link has been sent."}
    except Exception as exc:  # pragma: no cover - surfaced in UI
        return {"success": False, "error": str(exc)}


def logout_user(access_token: str | None = None) -> Dict[str, Any]:
    """Attempt to sign out a user by calling the Supabase logout endpoint.

    If `access_token` is not provided this function is a no-op and returns
    success so callers can clear UI state without requiring a token.
    """
    try:
        if not access_token:
            return {"success": True}
        url, key = _get_config()
        headers = {"apikey": key, "Authorization": f"Bearer {access_token}"}
        resp = httpx.post(f"{url}/auth/v1/logout", headers=headers, timeout=10.0)
        resp.raise_for_status()
        return {"success": True}
    except Exception as exc:  # pragma: no cover - surfaced in UI
        return {"success": False, "error": str(exc)}
