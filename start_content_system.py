#!/usr/bin/env python3
"""
Скрипт для запуска системы генерации контента
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_python_version():
    """Проверяет версию Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("🔍 Проверка зависимостей...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'aiogram', 'requests', 
        'pydantic', 'schedule', 'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите их командой: pip install -r telegram_autopost_bot/requirements.txt")
        return False
    
    return True

def setup_environment():
    """Настраивает окружение"""
    print("⚙️ Настройка окружения...")
    
    # Проверяем наличие .env файла
    env_file = Path("telegram_autopost_bot/.env")
    if not env_file.exists():
        print("⚠️ Файл .env не найден. Создайте его с настройками бота:")
        print("BOT_TOKEN=your_bot_token_here")
        print("ADMIN_ID=your_admin_id_here")
        return False
    
    print("✅ Файл .env найден")
    return True

def start_api_server():
    """Запускает API сервер"""
    print("🚀 Запуск API сервера...")
    
    try:
        # Переходим в папку бота
        os.chdir("telegram_autopost_bot")
        
        # Запускаем сервер в фоне
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "api:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ждем запуска сервера
        time.sleep(3)
        
        # Проверяем доступность
        try:
            response = requests.get("http://localhost:8000/api/stats", timeout=5)
            if response.status_code == 200:
                print("✅ API сервер запущен и доступен")
                return process
            else:
                print(f"❌ API сервер не отвечает: {response.status_code}")
                process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ API сервер не запустился")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return None

def test_content_generation():
    """Тестирует генерацию контента"""
    print("🧪 Тестирование генерации контента...")
    
    try:
        response = requests.post("http://localhost:8000/api/content/generate", json={
            "audience_group": "Новички в дизайне",
            "content_type": "Проблема",
            "channel_id": "test",
            "custom_prompt": ""
        })
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print("✅ Генерация контента работает")
                print(f"📝 Пример: {data['content'][:100]}...")
                return True
            else:
                print(f"❌ Ошибка генерации: {data.get('detail', 'Unknown')}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def open_dashboard():
    """Открывает дашборд в браузере"""
    print("🌐 Открытие дашборда...")
    
    try:
        import webbrowser
        webbrowser.open("http://localhost:8000")
        print("✅ Дашборд открыт в браузере")
    except Exception as e:
        print(f"⚠️ Не удалось открыть браузер: {e}")
        print("Откройте вручную: http://localhost:8000")

def main():
    """Основная функция"""
    print("🎨 Запуск системы генерации контента")
    print("=" * 50)
    
    # Проверки
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    if not setup_environment():
        return
    
    # Запуск сервера
    server_process = start_api_server()
    if not server_process:
        print("❌ Не удалось запустить сервер")
        return
    
    # Тестирование
    if not test_content_generation():
        print("❌ Генерация контента не работает")
        server_process.terminate()
        return
    
    # Открытие дашборда
    open_dashboard()
    
    print("\n" + "=" * 50)
    print("🎉 Система запущена успешно!")
    print("\n📋 Доступные функции:")
    print("• Генерация контента для 4 аудиторий")
    print("• 6 типов контента (проблемы, решения, кейсы и т.д.)")
    print("• Планирование постов")
    print("• Аналитика и статистика")
    print("• Веб-интерфейс для управления")
    
    print("\n🔗 Ссылки:")
    print("• Дашборд: http://localhost:8000")
    print("• API документация: http://localhost:8000/docs")
    
    print("\n⏹️ Для остановки нажмите Ctrl+C")
    
    try:
        # Держим сервер запущенным
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Остановка сервера...")
        server_process.terminate()
        print("✅ Сервер остановлен")

if __name__ == "__main__":
    main() 