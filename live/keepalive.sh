#!/usr/bin/env bash
#
# keepalive.sh
# Keeps an Oracle Always-Free VM from being reclaimed as "idle" by briefly
# loading one CPU core. Oracle deems an A1 instance idle only if CPU AND network
# AND memory are all < 20% (95th pct) over 7 days, so pushing CPU above 20% for
# a small fraction of the time is enough to stay alive. Run a few times a day by cron.
#
# Usage: keepalive.sh [burn_seconds]   (default 1800 = 30 min)

set -euo pipefail

readonly BURN_SECONDS="${1:-1800}"

main() {
  if command -v stress-ng >/dev/null 2>&1; then
    stress-ng --cpu 1 --timeout "${BURN_SECONDS}s"
  else
    # Fallback if stress-ng is unavailable: busy-loop one core for BURN_SECONDS.
    # 'timeout' exits 124 when it stops the loop, which is expected — swallow it.
    timeout "${BURN_SECONDS}" bash -c 'while :; do :; done' || true
  fi
}

main "$@"
