@echo off
cd /d "%~dp0\.."
if not exist ".venv\Scripts\python.exe" (
 echo Please run scripts\setup.bat first.
 pause
 exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m backend.main
pause
