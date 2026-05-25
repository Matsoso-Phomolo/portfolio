@echo off
cd /d "%~dp0backend"
set "CODEX_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%CODEX_PYTHON%" (
  "%CODEX_PYTHON%" -m uvicorn main:app --host 127.0.0.1 --port 8000
) else (
  python -m uvicorn main:app --host 127.0.0.1 --port 8000
)
