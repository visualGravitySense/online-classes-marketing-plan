#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the current directory
    current_dir = Path.cwd()
    bot_dir = current_dir / "telegram_autopost_bot"
    
    # Check if virtual environment exists
    venv_path = current_dir / "venv"
    if not venv_path.exists():
        print("Virtual environment not found. Please create one first.")
        return
    
    # Activate virtual environment and set Python path
    python_exe = venv_path / "Scripts" / "python.exe"
    if not python_exe.exists():
        print(f"Python executable not found at {python_exe}")
        return
    
    print("Starting all services...")
    
    # Start Telegram bot
    print("Starting Telegram Bot...")
    bot_process = subprocess.Popen([
        str(python_exe), "main.py"
    ], cwd=bot_dir)
    
    # Start API server
    print("Starting API Server...")
    api_process = subprocess.Popen([
        str(python_exe), "-m", "uvicorn", "api:app", "--reload"
    ], cwd=bot_dir, env={**os.environ, 'PYTHONPATH': str(bot_dir)})
    
    # Start HTTP server
    print("Starting HTTP Server...")
    http_process = subprocess.Popen([
        str(python_exe), "-m", "http.server", "8080"
    ], cwd=current_dir)
    
    print("All services started!")
    print("Press Ctrl+C to stop all services...")
    
    try:
        # Wait for all processes
        bot_process.wait()
        api_process.wait()
        http_process.wait()
    except KeyboardInterrupt:
        print("\nStopping all services...")
        bot_process.terminate()
        api_process.terminate()
        http_process.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    main() 