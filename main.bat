@echo off
chcp 65001 >nul

echo Running Python script...
python merge.py
if errorlevel 1 (
    echo Python script failed.
    pause
    exit /b
)

echo Adding files to git...
git add .

echo Committing...
git commit -m "update"
if errorlevel 1 (
    echo Nothing to commit or commit failed.
)

echo Pushing...
git push
if errorlevel 1 (
    echo Push failed.
    pause
    exit /b
)

echo Done!
pause