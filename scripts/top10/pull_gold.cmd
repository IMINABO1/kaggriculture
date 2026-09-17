@echo off
rem Detached runner for the gold-zone replay pull: loops pull_gold.py until it reports the cap
rem or nothing left, logging to data\gold\pull.log. Start with:
rem   powershell -c "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c scripts\top10\pull_gold.cmd'"
cd /d "%~dp0..\.."
set KAGG_WORKSPACE=data/gold
:loop
echo == pull_gold.cmd pass %date% %time% >> data\gold\pull.log
uv run python scripts\top10\pull_gold.py --cap-gb 10 --jobs 2 --sources endpoint --teams-first data\gold\teams_first.txt >> data\gold\pull.log 2>&1
findstr /c:"cap of" /c:"nothing left" data\gold\pull.log >nul && goto done
timeout /t 120 /nobreak >nul
goto loop
:done
echo == pull_gold.cmd done %date% %time% >> data\gold\pull.log
