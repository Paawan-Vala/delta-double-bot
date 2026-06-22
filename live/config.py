#!/usr/bin/env python3
"""Live config — load Delta Exchange credentials from .ENV. Secrets are never logged.

Expected variables in the project-root ``.ENV`` file (aliases accepted):

    DELTA_API_KEY=...        # or API_KEY / DELTA_KEY
    DELTA_API_SECRET=...     # or API_SECRET / DELTA_SECRET
    DELTA_BASE_URL=...       # optional; defaults to Testnet-India

Base URLs (from Delta docs):
    Testnet-India   : https://cdn-ind.testnet.deltaex.org   (demo / paper)
    Production-India: https://api.india.delta.exchange       (real money)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".ENV"

TESTNET_INDIA = "https://cdn-ind.testnet.deltaex.org"
PROD_INDIA = "https://api.india.delta.exchange"


@dataclass(frozen=True)
class DeltaCredentials:
    """Delta Exchange API credentials + endpoint."""

    api_key: str
    api_secret: str
    base_url: str

    @property
    def is_testnet(self) -> bool:
        """True when pointed at a testnet/demo endpoint."""
        return ("testnet" in self.base_url) or ("deltaex.org" in self.base_url)


def mask(secret: str) -> str:
    """Return a non-revealing preview of a secret for safe logging."""
    if not secret:
        return "<empty>"
    if len(secret) <= 8:
        return "*" * len(secret)
    return f"{secret[:4]}…{secret[-4:]} (len={len(secret)})"


def _first_env(*names: str) -> str:
    """Return the first non-empty environment variable among ``names``."""
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value.strip()
    return ""


def load_credentials(env_path: Path = ENV_PATH, account: str = "first") -> DeltaCredentials:
    """Load credentials from ``.ENV``; raise a clear error if any are missing.

    ``account="first"`` reads ``API_KEY`` / ``API_SECRET`` (the original account).
    ``account="second"`` reads ``API_KEY_SECOND`` / ``API_SECRET_SECOND`` (the demo account
    used for the double-diagonal bot). Both default to Testnet-India unless a base-url var is set.
    """
    load_dotenv(dotenv_path=env_path, override=False)
    if account == "second":
        api_key = _first_env("API_KEY_SECOND", "DELTA_API_KEY_SECOND", "DELTA_KEY_SECOND")
        api_secret = _first_env("API_SECRET_SECOND", "DELTA_API_SECRET_SECOND", "DELTA_SECRET_SECOND")
        base_url = _first_env("DELTA_BASE_URL_SECOND", "DELTA_BASE_URL", "BASE_URL") or TESTNET_INDIA
        key_name, secret_name = "API_KEY_SECOND", "API_SECRET_SECOND"
    else:
        api_key = _first_env("DELTA_API_KEY", "API_KEY", "DELTA_KEY")
        api_secret = _first_env("DELTA_API_SECRET", "API_SECRET", "DELTA_SECRET")
        base_url = _first_env("DELTA_BASE_URL", "BASE_URL") or TESTNET_INDIA
        key_name, secret_name = "DELTA_API_KEY", "DELTA_API_SECRET"

    missing = []
    if not api_key:
        missing.append(key_name)
    if not api_secret:
        missing.append(secret_name)
    if missing:
        raise RuntimeError(
            f"Missing {', '.join(missing)} in {env_path}. "
            f"Add them to your .ENV (see the template in live/config.py docstring)."
        )
    return DeltaCredentials(api_key=api_key, api_secret=api_secret, base_url=base_url)
