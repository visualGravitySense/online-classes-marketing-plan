#!/usr/bin/env python3
"""
Простой тест для проверки работы бота
"""

import os
import sys
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ALL_CHANNELS

load_dotenv()

def test_config():
    """Тест конфигурации"""
    print("🔍 ТЕСТ КОНФИГУРАЦИИ")
    print("=" * 40)
    
    # Проверяем токен
    bot_token = os.getenv('BOT_TOKEN')
    if bot_token:
        print(f"✅ BOT_TOKEN найден: {bot_token[:10]}...")
    else:
        print("❌ BOT_TOKEN не найден")
        return False
    
    # Проверяем каналы
    print(f"\n📋 Каналы в конфиге: {len(ALL_CHANNELS)}")
    
    campaigns = {}
    for channel_id, channel_data in ALL_CHANNELS.items():
        campaign = channel_data.get('campaign', 'default')
        if campaign not in campaigns:
            campaigns[campaign] = []
        campaigns[campaign].append(channel_data.get('name', 'Unknown'))
    
    print(f"\n🎯 Кампании:")
    for campaign, channels in campaigns.items():
        print(f"   • {campaign.upper()}: {len(channels)} каналов")
        for channel in channels:
            print(f"     - {channel}")
    
    return True

def test_api():
    """Тест API"""
    print("\n🌐 ТЕСТ API")
    print("=" * 40)
    
    try:
        import requests
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ API доступен")
            data = response.json()
            print(f"   Статус: {data.get('status')}")
            print(f"   Версия: {data.get('version')}")
            return True
        else:
            print(f"❌ API недоступен: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 ПРОСТОЙ ТЕСТ СИСТЕМЫ")
    print("=" * 50)
    
    # Тест конфигурации
    if not test_config():
        print("\n❌ Конфигурация не прошла тест")
        return
    
    # Тест API
    api_ok = test_api()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТА")
    print("=" * 50)
    
    if api_ok:
        print("✅ Все тесты пройдены!")
        print("\n💡 Для тестирования публикации используйте:")
        print("   python telegram_autopost_bot/quick_test_posting.py")
    else:
        print("⚠️ API недоступен")
        print("\n💡 Запустите API сервер:")
        print("   python telegram_autopost_bot/api.py")

if __name__ == "__main__":
    main() 