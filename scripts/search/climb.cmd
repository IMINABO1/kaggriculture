@echo off
rem Detached runner for the parameter search (see climb.py). Start with:
rem   powershell -c "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c scripts\search\climb.cmd'"
cd /d "%~dp0..\.."
echo == climb.cmd start %date% %time% >> results\search.log
uv run python -u scripts\search\climb.py --hours 3 --jobs 4 >> results\search.log 2>&1
echo == climb.cmd done %date% %time% >> results\search.log
