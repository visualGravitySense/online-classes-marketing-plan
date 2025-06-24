#!/usr/bin/env python3
"""
Тест публикации только в рабочие каналы
"""

import os
import sys
import asyncio
import json
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot

load_dotenv()

async def send_test_post(bot: Bot, channel_id: str, channel_name: str, campaign: str):
    """Отправка тестового поста"""
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

async def test_working_channels():
    """Тест только рабочих каналов"""
    print("🚀 ТЕСТ ПУБЛИКАЦИИ В РАБОЧИЕ КАНАЛЫ")
    print("=" * 60)
    
    # Проверяем токен
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не найден в .env файле")
        return
    
    # Создаем бота
    bot = Bot(token=bot_token)
    
    # Загружаем рабочие каналы
    try:
        with open('working_channels.json', 'r', encoding='utf-8') as f:
            working_channels = json.load(f)
    except FileNotFoundError:
        print("❌ Файл working_channels.json не найден")
        print("💡 Сначала запустите: python telegram_autopost_bot/check_channels.py")
        return
    
    print(f"📋 Загружено рабочих каналов: {len(working_channels)}")
    
    # Группируем по кампаниям
    campaigns = {}
    for channel_key, channel_data in working_channels.items():
        campaign = channel_data.get('campaign', 'default')
        if campaign not in campaigns:
            campaigns[campaign] = []
        campaigns[campaign].append((channel_data['chat_id'], channel_data['name'], channel_data))
    
    # Тестируем каждую кампанию
    total_success = 0
    total_errors = 0
    
    for campaign, channels in campaigns.items():
        print(f"\n🎯 КАМПАНИЯ: {campaign.upper()}")
        print("-" * 40)
        
        campaign_success = 0
        campaign_errors = 0
        
        for channel_id, channel_name, channel_data in channels:
            print(f"\n📢 Канал: {channel_name}")
            print(f"   ID: {channel_id}")
            
            result = await send_test_post(bot, channel_id, channel_name, campaign)
            
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
            await asyncio.sleep(2)
        
        print(f"\n📊 Результат кампании {campaign.upper()}:")
        print(f"   ✅ Успешно: {campaign_success}")
        print(f"   ❌ Ошибок: {campaign_errors}")
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    print(f"🎯 Всего каналов: {len(working_channels)}")
    print(f"✅ Успешно: {total_success}")
    print(f"❌ Ошибок: {total_errors}")
    
    if total_errors == 0:
        print("🎉 Все тесты пройдены успешно!")
        print("🎯 Универсальный бот работает корректно!")
    else:
        print("⚠️ Есть ошибки, но большинство каналов работают")
    
    # Закрываем бота
    await bot.session.close()

def main():
    """Основная функция"""
    asyncio.run(test_working_channels())

if __name__ == "__main__":
    main() 