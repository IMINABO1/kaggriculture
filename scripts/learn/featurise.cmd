@echo off
rem Detached runner for the featuriser: follows the gold pull, two workers, logging to
rem data\features\featurise.log. Start with:
rem   powershell -c "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c scripts\learn\featurise.cmd'"
cd /d "%~dp0..\.."
set KAGG_WORKSPACE=data/gold
if not exist data\features mkdir data\features
echo == featurise.cmd start %date% %time% >> data\features\featurise.log
uv run python scripts\learn\featurise.py --jobs 2 --watch 600 >> data\features\featurise.log 2>&1
echo == featurise.cmd exit %date% %time% >> data\features\featurise.log
