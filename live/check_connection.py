#!/usr/bin/env python3
"""Read-only Delta Exchange connection check. Places NO orders.

Validates that your .ENV credentials authenticate against the (testnet) API and that
market data is reachable. Run this first, before building any execution logic.

Usage:
    python -m live.check_connection
    python -m live.check_connection -v
"""
from __future__ import annotations

import argparse
import logging
import sys

import requests

from live.config import load_credentials, mask

logger = logging.getLogger(__name__)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
PERP_SYMBOL = "BTCUSD"


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Read-only Delta Exchange connection check (no orders).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser


def configure_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def _count_option_products(base_url: str) -> tuple[int, int]:
    """Return (num_calls, num_puts) from the public products endpoint."""
    resp = requests.get(f"{base_url}/v2/products", timeout=20)
    resp.raise_for_status()
    products = resp.json().get("result", [])
    calls = sum(1 for p in products if p.get("contract_type") == "call_options")
    puts = sum(1 for p in products if p.get("contract_type") == "put_options")
    return calls, puts


def run() -> int:
    """Run the read-only checks and report PASS/FAIL for each."""
    creds = load_credentials()
    logger.info("Endpoint : %s  (%s)", creds.base_url, "TESTNET/demo" if creds.is_testnet else "PRODUCTION")
    logger.info("API key  : %s", mask(creds.api_key))
    logger.info("API secret: %s", mask(creds.api_secret))

    from delta_rest_client import DeltaRestClient

    client = DeltaRestClient(base_url=creds.base_url, api_key=creds.api_key, api_secret=creds.api_secret)
    ok = True

    # 1) Public market data — futures ticker.
    try:
        ticker = client.get_ticker(PERP_SYMBOL)
        result = ticker.get("result", ticker) if isinstance(ticker, dict) else {}
        price = result.get("mark_price") or result.get("close") or result.get("spot_price")
        logger.info("PASS  market data: %s mark/last = %s", PERP_SYMBOL, price)
    except Exception as exc:  # noqa: BLE001
        ok = False
        logger.error("FAIL  market data (get_ticker): %s", exc)

    # 2) Public products — options chain availability.
    try:
        calls, puts = _count_option_products(creds.base_url)
        logger.info("PASS  options chain: %d calls / %d puts listed", calls, puts)
    except Exception as exc:  # noqa: BLE001
        logger.warning("WARN  options chain listing failed: %s", exc)

    # 3) Authenticated (signed) call — confirms the key/secret are valid. No orders placed.
    try:
        orders = client.get_live_orders()
        n = len(orders) if isinstance(orders, list) else len(orders.get("result", []))
        logger.info("PASS  authentication: signed request OK (%d open orders)", n)
    except Exception as exc:  # noqa: BLE001
        ok = False
        logger.error("FAIL  authentication (get_live_orders): %s", exc)
        logger.error("      -> check the API key/secret, IP whitelist, and 'Trading' permission.")

    logger.info("RESULT: %s", "ALL GOOD — safe to build execution next." if ok else "issues above need fixing.")
    return EXIT_SUCCESS if ok else EXIT_FAILURE


def main() -> int:
    """Main entry point."""
    args = create_parser().parse_args()
    configure_logging(args.verbose)
    try:
        return run()
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        logger.exception("Failed: %s", exc)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
