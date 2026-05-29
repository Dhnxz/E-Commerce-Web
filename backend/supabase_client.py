"""Supabase client helper.

This module uses the Supabase REST endpoints directly so it works with
publishable keys without the stricter JWT validation in older Python SDKs.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv


load_dotenv()


@dataclass
class _Response:
    data: Any


class _RPCRequest:
    def __init__(self, base_url: str, headers: Dict[str, str], function_name: str, params: Dict[str, Any]):
        self.base_url = base_url
        self.headers = headers
        self.function_name = function_name
        self.params = params

    def execute(self) -> _Response:
        url = f"{self.base_url}/rest/v1/rpc/{self.function_name}"
        response = httpx.post(url, headers=self.headers, json=self.params, timeout=30.0)
        response.raise_for_status()
        return _Response(response.json())


def _build_headers(api_key: str) -> Dict[str, str]:
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


class SupabaseClient:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

        self.base_url = self.url.rstrip("/")
        self.headers = _build_headers(self.key)
        self.client = httpx.Client(timeout=30.0)

    def get_table(self, table: str) -> List[Dict[str, Any]]:
        """Return all rows from a table as a list of dicts."""
        url = f"{self.base_url}/rest/v1/{table}"
        response = self.client.get(url, headers=self.headers, params={"select": "*"})
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()

    def query(self, sql: str) -> Any:
        """Kept for compatibility; use `rpc()` for database functions."""
        raise NotImplementedError("Use rpc() with a database function instead.")

    def rpc(self, function_name: str, params: Optional[Dict[str, Any]] = None) -> _RPCRequest:
        """Call a Postgres function exposed by Supabase."""
        return _RPCRequest(self.base_url, self.headers, function_name, params or {})


def main() -> None:
    """Small smoke test for local execution."""
    client = get_supabase_client()
    _ = client
    print("Supabase Connected Successfully!")


def get_supabase_client(url: Optional[str] = None, key: Optional[str] = None):
    """Create a Supabase-compatible client from explicit values or environment variables."""
    return SupabaseClient(url, key)


if __name__ == "__main__":
    main()
