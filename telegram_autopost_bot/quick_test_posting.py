#!/usr/bin/env python3
"""
Быстрый тест публикации во все каналы
Работает напрямую с ботом, без API
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ALL_CHANNELS, POST_TEMPLATES
from database import Database
from aiogram import Bot

load_dotenv()

async def send_test_post_direct(bot: Bot, channel_id: str, channel_name: str, campaign: str):
    """Прямая отправка тестового поста"""
    try:
        # Генерируем контент
        if campaign == 'digitalizacija':
            content = f"""
🎯 ТЕСТОВЫЙ ПОСТ - Цифровизация бизнеса

📝 Это тестовый пост для проверки работы универсального бота.
Канал: {channel_name}
Кампания: {campaign.upper()}

💡 Практический совет: Автоматизируйте рутинные задачи

📊 85% компаний экономят время благодаря цифровизации

❓ Какие процессы в вашем бизнесе можно автоматизировать?

#цифровизация #бизнес #автоматизация #тест
            """.strip()
        else:
            content = f"""
💡 ТЕСТОВЫЙ ПОСТ - UX/UI Дизайн

Это тестовый пост для проверки работы универсального бота.
Канал: {channel_name}
Кампания: {campaign.upper()}

🔖 Сохраняй пост, чтобы не потерять!
💬 Делись своим мнением в комментариях

#UXUITips #Дизайн #Обучение #тест
            """.strip()
        
        # Отправляем пост
        await bot.send_message(chat_id=channel_id, text=content)
        return {'status': 'success', 'message': f"Пост отправлен в {channel_name}"}
        
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'message': f"Ошибка отправки в {channel_name}"}

async def quick_test_all_channels():
    """Быстрый тест всех каналов"""
    print("🚀 БЫСТРЫЙ ТЕСТ ПУБЛИКАЦИИ ВО ВСЕ КАНАЛЫ")
    print("=" * 60)
    
    # Проверяем токен
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не найден в .env файле")
        return
    
    # Создаем бота
    bot = Bot(token=bot_token)
    
    # Получаем активные каналы
    active_channels = {}
    for channel_id, channel_data in ALL_CHANNELS.items():
        if channel_data.get('active', True):
            active_channels[channel_id] = channel_data
    
    print(f"📋 Найдено активных каналов: {len(active_channels)}")
    
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
            
            result = await send_test_post_direct(bot, channel_id, channel_name, campaign)
            
            if result['status'] == 'success':
                campaign_success += 1
                total_success += 1
                print(f"   ✅ {result['message']}")
            else:
                campaign_errors += 1
                total_errors += 1
                print(f"   ❌ {result['message']}")
                print(f"   🔍 Ошибка: {result['error']}")
            
            # Небольшая задержка между постами
            await asyncio.sleep(1)
        
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
    else:
        print("⚠️ Есть ошибки, проверьте настройки каналов")
    
    # Закрываем бота
    await bot.session.close()

def main():
    """Основная функция"""
    asyncio.run(quick_test_all_channels())

if __name__ == "__main__":
    main() 