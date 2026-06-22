#!/usr/bin/env python3
"""Phase 3a — Black-76 pricing for European options on a futures price.

Delta Exchange BTC options are priced in USD against the BTCUSD future, so Black-76
(options on a forward/future) is the right model. Used in the backtest to:

* imply a volatility from observed option trades, and
* price an option leg on days when it did not trade (fallback), and
* estimate delta for moneyness/strike selection.

All prices are in USD per 1 BTC of notional; multiply by contracts * lot size for cash.
"""
from __future__ import annotations

import math


def _norm_cdf(x: float) -> float:
    """Standard normal CDF via the error function (no SciPy dependency)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _d1_d2(f: float, k: float, t: float, sigma: float) -> tuple[float, float]:
    """Black-76 d1 and d2."""
    srt = sigma * math.sqrt(t)
    d1 = (math.log(f / k) + 0.5 * sigma * sigma * t) / srt
    return d1, d1 - srt


def intrinsic(f: float, k: float, is_call: bool) -> float:
    """Undiscounted intrinsic value."""
    return max(f - k, 0.0) if is_call else max(k - f, 0.0)


def black76_price(f: float, k: float, t: float, sigma: float, r: float, is_call: bool) -> float:
    """Black-76 option price (USD) on a future ``f`` with strike ``k``.

    ``t`` is time to expiry in years, ``sigma`` annualised vol, ``r`` the rate.
    """
    if t <= 0.0 or sigma <= 0.0 or f <= 0.0 or k <= 0.0:
        return math.exp(-r * max(t, 0.0)) * intrinsic(f, k, is_call)
    d1, d2 = _d1_d2(f, k, t, sigma)
    disc = math.exp(-r * t)
    if is_call:
        return disc * (f * _norm_cdf(d1) - k * _norm_cdf(d2))
    return disc * (k * _norm_cdf(-d2) - f * _norm_cdf(-d1))


def black76_delta(f: float, k: float, t: float, sigma: float, r: float, is_call: bool) -> float:
    """Black-76 delta (with respect to the future)."""
    if t <= 0.0 or sigma <= 0.0:
        itm = (f > k) if is_call else (f < k)
        if is_call:
            return 1.0 if itm else 0.0
        return -1.0 if itm else 0.0
    d1, _ = _d1_d2(f, k, t, sigma)
    disc = math.exp(-r * t)
    return disc * _norm_cdf(d1) if is_call else -disc * _norm_cdf(-d1)


def black76_implied_vol(
    price: float, f: float, k: float, t: float, r: float, is_call: bool,
    lo: float = 1e-4, hi: float = 5.0, tol: float = 1e-6, max_iter: int = 100,
) -> float:
    """Implied vol via bisection; returns NaN if the price is below intrinsic."""
    if t <= 0.0 or price <= 0.0:
        return math.nan
    disc_intrinsic = math.exp(-r * t) * intrinsic(f, k, is_call)
    if price <= disc_intrinsic + 1e-9:
        return math.nan

    f_lo = black76_price(f, k, t, lo, r, is_call) - price
    f_hi = black76_price(f, k, t, hi, r, is_call) - price
    if f_lo * f_hi > 0.0:
        return math.nan  # not bracketed

    a, b = lo, hi
    for _ in range(max_iter):
        mid = 0.5 * (a + b)
        fm = black76_price(f, k, t, mid, r, is_call) - price
        if abs(fm) < tol:
            return mid
        if (black76_price(f, k, t, a, r, is_call) - price) * fm <= 0.0:
            b = mid
        else:
            a = mid
    return 0.5 * (a + b)


if __name__ == "__main__":
    # Tiny self-check: round-trip price -> implied vol -> price.
    f0, k0, t0, sig0, r0 = 80000.0, 80000.0, 30 / 365.0, 0.6, 0.0
    px = black76_price(f0, k0, t0, sig0, r0, is_call=False)
    iv = black76_implied_vol(px, f0, k0, t0, r0, is_call=False)
    print(f"price={px:.2f} implied_vol={iv:.4f} delta={black76_delta(f0, k0, t0, sig0, r0, False):.3f}")
