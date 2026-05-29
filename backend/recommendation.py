"""Recommendation logic backed by Supabase/Postgres.

This module calls the `get_recommendations` database function defined in
`database/schema.sql`. That keeps the ranking logic close to the data and
lets the app work once `products` and `interactions` are populated.
"""

import os
from typing import Any, Dict, List

from dotenv import load_dotenv

from backend.supabase_client import SupabaseClient


load_dotenv()


def _get_client() -> SupabaseClient:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY in environment")
    return SupabaseClient(url, key)


def recommend(user_id: int, top_k: int = 10) -> List[int]:
    """Return top_k recommended product ids for `user_id`.

    The underlying SQL function returns popularity-ranked products while
    excluding any items the user has already interacted with.
    """
    client = _get_client()

    try:
        response = client.rpc("get_recommendations", {"p_user_id": int(user_id), "p_limit": int(top_k)}).execute()
    except Exception:
        return []

    rows: List[Dict[str, Any]] = getattr(response, "data", []) or []

    return [int(row["product_id"]) for row in rows if row.get("product_id") is not None]
