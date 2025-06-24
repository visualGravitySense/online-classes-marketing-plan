#!/usr/bin/env python3
"""
Тестовый скрипт для проверки исправлений ботов
"""

import os
import sys
import time

def test_universal_bot():
    """Тестирование universal_bot.py"""
    print("🧪 Тестирование universal_bot.py...")
    
    try:
        # Добавляем путь к папке с ботом
        bot_path = os.path.join(os.path.dirname(__file__), 'telegram_autopost_bot')
        sys.path.insert(0, bot_path)
        
        # Импортируем и создаем экземпляр бота
        from universal_bot import UniversalBot
        
        bot = UniversalBot()
        print("✅ universal_bot.py работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в universal_bot.py: {e}")
        return False

def test_main_bot():
    """Тестирование main.py"""
    print("🧪 Тестирование main.py...")
    
    try:
        # Добавляем путь к папке с ботом
        bot_path = os.path.join(os.path.dirname(__file__), 'telegram_autopost_bot')
        sys.path.insert(0, bot_path)
        
        # Импортируем и создаем экземпляр бота
        from main import TelegramBot
        
        bot = TelegramBot()
        print("✅ main.py работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в main.py: {e}")
        return False

def test_scheduler():
    """Тестирование scheduler.py"""
    print("🧪 Тестирование scheduler.py...")
    
    try:
        # Добавляем путь к папке с ботом
        bot_path = os.path.join(os.path.dirname(__file__), 'telegram_autopost_bot')
        sys.path.insert(0, bot_path)
        
        # Импортируем планировщик
        from scheduler import PostScheduler
        from database import Database
        from aiogram import Bot
        
        # Создаем тестовый экземпляр (игнорируем ошибку токена)
        db = Database('data/posts.db')
        
        # Создаем бота с тестовым токеном (не проверяем валидность)
        bot = Bot(token="test_token", validate_token=False)
        scheduler = PostScheduler(db, bot, {})
        
        print("✅ scheduler.py работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в scheduler.py: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🔧 Тестирование исправлений ботов")
    print("=" * 40)
    
    results = []
    
    # Тестируем каждый компонент
    results.append(test_universal_bot())
    results.append(test_main_bot())
    results.append(test_scheduler())
    
    print("\n" + "=" * 40)
    print("📊 Результаты тестирования:")
    
    if all(results):
        print("🎉 Все тесты пройдены! Боты готовы к запуску.")
        print("\n🚀 Теперь можно запускать:")
        print("   python start_universal_bot_system.py")
        print("   или")
        print("   cd telegram_autopost_bot && python main.py")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте ошибки выше.")
    
    return all(results)

if __name__ == "__main__":
    main() 