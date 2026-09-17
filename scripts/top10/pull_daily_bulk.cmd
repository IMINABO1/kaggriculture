@echo off
rem Detached runner for the daily-archive import (see pull_daily_bulk.py). Start with:
rem   powershell -c "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c scripts\top10\pull_daily_bulk.cmd'"
cd /d "%~dp0..\.."
set KAGG_WORKSPACE=data/gold
echo == pull_daily_bulk.cmd start %date% %time% >> data\gold\daily_bulk.log
uv run python -u scripts\top10\pull_daily_bulk.py >> data\gold\daily_bulk.log 2>&1
echo == pull_daily_bulk.cmd done %date% %time% >> data\gold\daily_bulk.log
