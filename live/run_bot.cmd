@echo off
REM Launcher for the live PMCP bot, used by Windows Task Scheduler.
REM Runs ONE decision cycle (open / roll / close) on testnet and appends to live\bot.log.
cd /d "E:\Paawan\Trading Algo\Options"
echo ============ %DATE% %TIME% ============ >> "live\bot.log"
".\.venv\Scripts\python.exe" -m live.runner --execute --contracts 1 >> "live\bot.log" 2>&1
