@echo off
rem  TOTALCONTROL CORE (FREE) — start and go. State law: no hands, no memory,
rem  no crawl. Gateway binds 127.0.0.1:8792 ONLY.
setlocal
set PROJ=%~dp0
set PY=%PROJ%.venv\Scripts\python.exe
echo.
echo   TOTALCONTROL CORE  (FREE BUILD)
echo   bind: 127.0.0.1:8792 (local-only law)
echo.
if not exist "%PY%" ( echo   venv missing - AI-INSTALL.md step 2 first & pause & exit /b 1 )
start "TOTALCONTROL-CORE" /D "%PROJ%" "%PY%" server_core.py
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8792/core
endlocal
