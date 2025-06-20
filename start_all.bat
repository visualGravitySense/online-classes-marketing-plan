@echo off
echo Starting all services...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the Telegram bot
start "Telegram Bot" cmd /k "call venv\Scripts\activate.bat && cd telegram_autopost_bot && python main.py"

REM Start the API server (run from telegram_autopost_bot directory with proper Python path)
start "API Server" cmd /k "call venv\Scripts\activate.bat && cd telegram_autopost_bot && set PYTHONPATH=. && python -m uvicorn api:app --reload"

REM Start the HTTP server
start "HTTP Server" cmd /k "call venv\Scripts\activate.bat && python -m http.server 8080"

echo All services started in separate windows.
pause 