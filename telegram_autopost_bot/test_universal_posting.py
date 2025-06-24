#!/usr/bin/env python3
"""
Тестовый скрипт для публикации во все каналы универсального бота
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ALL_CHANNELS, POST_TEMPLATES

load_dotenv()

def generate_test_content(campaign: str, channel_name: str) -> str:
    """Генерация тестового контента"""
    if campaign == 'digitalizacija':
        return f"""
🎯 ТЕСТОВЫЙ ПОСТ - Цифровизация бизнеса

📝 Это тестовый пост для проверки работы универсального бота.
Канал: {channel_name}
Кампания: {campaign.upper()}

💡 Практический совет: Автоматизируйте рутинные задачи

📊 85% компаний экономят время благодаря цифровизации

❓ Какие процессы в вашем бизнесе можно автоматизировать?

#цифровизация #бизнес #автоматизация #тест
        """.strip()
    
    else:  # default (UXUI)
        return f"""
💡 ТЕСТОВЫЙ ПОСТ - UX/UI Дизайн

Это тестовый пост для проверки работы универсального бота.
Канал: {channel_name}
Кампания: {campaign.upper()}

🔖 Сохраняй пост, чтобы не потерять!
💬 Делись своим мнением в комментариях

#UXUITips #Дизайн #Обучение #тест
        """.strip()

def send_test_post(channel_id: str, channel_name: str, campaign: str) -> dict:
    """Отправка тестового поста"""
    try:
        content = generate_test_content(campaign, channel_name)
        scheduled_time = datetime.now() + timedelta(minutes=2)
        
        post_data = {
            "content": content,
            "channel_id": channel_id,
            "scheduled_time": scheduled_time.isoformat(),
            "media_path": None,
            "media_type": None
        }
        
        response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'status': 'success',
                'post_id': result.get('post_id'),
                'message': f"Пост запланирован в {channel_name}"
            }
        else:
            return {
                'status': 'error',
                'error': f"API ошибка {response.status_code}",
                'message': f"Ошибка отправки в {channel_name}"
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': f"Ошибка отправки в {channel_name}"
        }

def test_all_channels():
    """Тестирование всех каналов"""
    print("🚀 ТЕСТИРОВАНИЕ ПУБЛИКАЦИИ ВО ВСЕ КАНАЛЫ")
    print("=" * 60)
    
    # Проверяем API
    try:
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code != 200:
            print("❌ API недоступен. Запустите API сервер:")
            print("   python telegram_autopost_bot/api.py")
            return
    except Exception as e:
        print(f"❌ API недоступен: {e}")
        return
    
    print("✅ API доступен")
    
    # Получаем активные каналы
    active_channels = {}
    for channel_id, channel_data in ALL_CHANNELS.items():
        if channel_data.get('active', True):
            active_channels[channel_id] = channel_data
    
    print(f"\n📋 Найдено активных каналов: {len(active_channels)}")
    
    # Группируем по кампаниям
    campaigns = {}
    for channel_id, channel_data in active_channels.items():
        campaign = channel_data.get('campaign', 'default')
        if campaign not in campaigns:
            campaigns[campaign] = []
        campaigns[campaign].append((channel_id, channel_data))
    
    # Тестируем каждую кампанию
    total_success = 0
    total_errors = 0
    
    for campaign, channels in campaigns.items():
        print(f"\n🎯 КАМПАНИЯ: {campaign.upper()}")
        print("-" * 40)
        
        campaign_success = 0
        campaign_errors = 0
        
        for channel_id, channel_data in channels:
            channel_name = channel_data.get('name', 'Unknown')
            print(f"\n📢 Канал: {channel_name}")
            
            result = send_test_post(channel_id, channel_name, campaign)
            
            if result['status'] == 'success':
                campaign_success += 1
                total_success += 1
                print(f"   ✅ {result['message']}")
                print(f"   📝 ID поста: {result['post_id']}")
            else:
                campaign_errors += 1
                total_errors += 1
                print(f"   ❌ {result['message']}")
                print(f"   🔍 Ошибка: {result['error']}")
        
        print(f"\n📊 Результат кампании {campaign.upper()}:")
        print(f"   ✅ Успешно: {campaign_success}")
        print(f"   ❌ Ошибок: {campaign_errors}")
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    print(f"🎯 Всего каналов: {len(active_channels)}")
    print(f"✅ Успешно: {total_success}")
    print(f"❌ Ошибок: {total_errors}")
    
    if total_errors == 0:
        print("🎉 Все тесты пройдены успешно!")
        print("📝 Посты будут опубликованы через 2 минуты")
    else:
        print("⚠️ Есть ошибки, проверьте настройки каналов")

if __name__ == "__main__":
    test_all_channels() 