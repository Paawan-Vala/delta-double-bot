#!/usr/bin/env bash
#
# setup_vm.sh
# One-time bootstrap for the live double-diagonal bot on an Oracle (Ubuntu) VM.
# Installs system + Python dependencies and wires up cron (hourly trade cycle +
# CPU keep-alive). Idempotent — safe to re-run.
#
# Run once from the repo root after copying live/ and .ENV onto the VM:
#   bash live/setup_vm.sh

set -euo pipefail

main() {
  local script_dir repo_root trade_line keepalive_line cron_tmp
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  repo_root="$(cd "${script_dir}/.." && pwd)"
  cd "${repo_root}"
  echo "==> Repo root: ${repo_root}"

  # 1. System packages: Python venv support + stress-ng (keep-alive).
  echo "==> Installing system packages (needs sudo)…"
  sudo apt-get update -y
  sudo apt-get install -y python3-venv stress-ng

  # 2. Virtual environment + minimal runtime dependencies.
  if [[ ! -d .venv ]]; then
    echo "==> Creating virtualenv at .venv…"
    python3 -m venv .venv
  fi
  echo "==> Installing Python dependencies…"
  ./.venv/bin/python -m pip install --upgrade pip
  ./.venv/bin/python -m pip install -r live/requirements-live.txt

  # 3. Permissions.
  chmod +x live/run_double.sh live/keepalive.sh
  if [[ -f .ENV ]]; then
    chmod 600 .ENV
    echo "==> .ENV found and locked to 600."
  else
    echo "!! WARNING: .ENV not found at ${repo_root}/.ENV — copy it before going live."
  fi

  # 4. Cron: hourly trade cycle (:25) + CPU keep-alive every 6h. Installed idempotently.
  trade_line="25 * * * * ${repo_root}/live/run_double.sh"
  keepalive_line="0 */6 * * * ${repo_root}/live/keepalive.sh"
  cron_tmp="$(mktemp)"
  crontab -l 2>/dev/null \
    | grep -v -F "live/run_double.sh" \
    | grep -v -F "live/keepalive.sh" > "${cron_tmp}" || true
  {
    echo "${trade_line}"
    echo "${keepalive_line}"
  } >> "${cron_tmp}"
  crontab "${cron_tmp}"
  rm -f "${cron_tmp}"
  echo "==> Cron installed:"
  echo "      ${trade_line}"
  echo "      ${keepalive_line}"

  # 5. Dry-run smoke test (no orders placed).
  echo "==> Dry-run smoke test (no orders)…"
  ./.venv/bin/python -m live.runner_double || true

  echo
  echo "==> Setup complete."
  echo "    Confirm the dry-run above connected and reconciled your 4 legs."
  echo "    Live cycles run hourly at :25 UTC. Logs: ${repo_root}/live/bot_double.log"
}

main "$@"
