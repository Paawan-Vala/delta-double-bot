#!/usr/bin/env bash
#
# run_double.sh
# Cron launcher for the live double-diagonal (PMCC+PMCP) bot on account 2.
# Runs ONE decision cycle (open / repair / roll / close) and appends to
# live/bot_double.log. Invoked hourly by cron on the Oracle VM.

set -euo pipefail

main() {
  local script_dir repo_root
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  repo_root="$(cd "${script_dir}/.." && pwd)"
  cd "${repo_root}"

  echo "============ $(date -u '+%Y-%m-%d %H:%M:%S') UTC ============" >> live/bot_double.log
  ./.venv/bin/python -m live.runner_double \
    --execute --contracts 1 --leverage 3 --margin-mode cross \
    >> live/bot_double.log 2>&1
}

main "$@"
