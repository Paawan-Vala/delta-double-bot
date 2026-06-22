@echo off
REM Launcher for the live DOUBLE (PMCC+PMCP) bot on account 2 (demo), used by Windows Task Scheduler.
REM Runs ONE 4-leg decision cycle (open / repair / roll / close) on testnet and appends to live\bot_double.log.
cd /d "E:\Paawan\Trading Algo\Options"
echo ============ %DATE% %TIME% ============ >> "live\bot_double.log"
".\.venv\Scripts\python.exe" -m live.runner_double --execute --contracts 1 --leverage 3 --margin-mode cross >> "live\bot_double.log" 2>&1
