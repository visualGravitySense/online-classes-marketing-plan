#!/usr/bin/env python3
"""
Скрипт для запуска интегрированной системы универсального бота
Включает в себя:
- API сервер с фронтендом
- Универсальный бот (опционально)
- Интеграцию между компонентами
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

def check_dependencies():
    """Проверка зависимостей"""
    print("🔍 Проверка зависимостей...")
    
    required_files = [
        'main_api.py',
        'telegram_autopost_bot/universal_bot.py',
        'telegram_autopost_bot/bot_integration.py',
        'telegram_autopost_bot/config.py',
        'telegram_autopost_bot/database.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Отсутствуют необходимые файлы:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Все зависимости найдены")
    return True

def check_env_file():
    """Проверка файла .env"""
    print("🔍 Проверка конфигурации...")
    
    env_file = 'telegram_autopost_bot/.env'
    if not os.path.exists(env_file):
        print(f"⚠️  Файл {env_file} не найден")
        print("   Создайте файл .env в папке telegram_autopost_bot/")
        print("   Пример содержимого:")
        print("   BOT_TOKEN=your_bot_token_here")
        print("   ADMIN_ID=your_admin_id_here")
        return False
    
    print("✅ Файл .env найден")
    return True

def start_api_server():
    """Запуск API сервера"""
    print("🚀 Запуск API сервера...")
    
    try:
        # Запускаем Flask сервер
        subprocess.run([
            sys.executable, 'main_api.py'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска API сервера: {e}")
        return False
    except KeyboardInterrupt:
        print("⏹️  API сервер остановлен")
        return True

def start_universal_bot():
    """Запуск универсального бота"""
    print("🤖 Запуск универсального бота...")
    
    try:
        # Переходим в папку с ботом
        os.chdir('telegram_autopost_bot')
        
        # Запускаем бота
        subprocess.run([
            sys.executable, 'universal_bot.py'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска бота: {e}")
        return False
    except KeyboardInterrupt:
        print("⏹️  Бот остановлен")
        return True
    finally:
        # Возвращаемся в корневую папку
        os.chdir('..')

def start_bot_in_background():
    """Запуск бота в фоновом режиме"""
    print("🤖 Запуск универсального бота в фоновом режиме...")
    
    def run_bot():
        try:
            os.chdir('telegram_autopost_bot')
            subprocess.run([
                sys.executable, 'universal_bot.py'
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка запуска бота: {e}")
        finally:
            os.chdir('..')
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    return bot_thread

def main():
    """Основная функция"""
    print("🎯 Запуск интегрированной системы универсального бота")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        print("❌ Не удалось запустить систему из-за отсутствующих зависимостей")
        return
    
    # Проверяем конфигурацию
    if not check_env_file():
        print("⚠️  Система будет работать в тестовом режиме без реального бота")
    
    print("\n📋 Доступные режимы запуска:")
    print("1. Только API сервер (фронтенд)")
    print("2. API сервер + бот в фоновом режиме")
    print("3. Только бот")
    print("4. Полная система (API + бот)")
    
    try:
        choice = input("\nВыберите режим (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
        return
    
    if choice == "1":
        print("\n🚀 Запуск только API сервера...")
        start_api_server()
    
    elif choice == "2":
        print("\n🚀 Запуск API сервера с ботом в фоне...")
        bot_thread = start_bot_in_background()
        time.sleep(2)  # Даем боту время на запуск
        start_api_server()
    
    elif choice == "3":
        print("\n🤖 Запуск только бота...")
        start_universal_bot()
    
    elif choice == "4":
        print("\n🚀 Запуск полной системы...")
        print("Запускаем бота в фоновом режиме...")
        bot_thread = start_bot_in_background()
        time.sleep(3)  # Даем боту время на запуск
        print("Запускаем API сервер...")
        start_api_server()
    
    else:
        print("❌ Неверный выбор. Запускаем только API сервер...")
        start_api_server()

def show_help():
    """Показать справку"""
    print("""
🎯 Интегрированная система универсального бота

Использование:
    python start_universal_bot_system.py

Режимы запуска:
    1. Только API сервер - для работы с фронтендом
    2. API + бот в фоне - полная система
    3. Только бот - для работы через Telegram
    4. Полная система - API + бот

Требования:
    - Python 3.7+
    - Файл .env в папке telegram_autopost_bot/
    - Все необходимые зависимости

Доступ к фронтенду:
    http://localhost:5000

Доступ к API:
    http://localhost:5000/api/universal-bot/...
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        main() 