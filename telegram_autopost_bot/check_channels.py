#!/usr/bin/env python3
"""
Скрипт для проверки и обновления ID каналов
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import ALL_CHANNELS
from aiogram import Bot

load_dotenv()

async def check_channel_access(bot: Bot, channel_id: str, channel_name: str):
    """Проверка доступа к каналу"""
    try:
        # Пытаемся получить информацию о канале
        chat = await bot.get_chat(channel_id)
        return {
            'status': 'success',
            'chat_id': chat.id,
            'title': chat.title,
            'username': chat.username,
            'type': chat.type
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'chat_id': channel_id
        }

async def check_all_channels():
    """Проверка всех каналов"""
    print("🔍 ПРОВЕРКА ДОСТУПА К КАНАЛАМ")
    print("=" * 60)
    
    # Проверяем токен
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не найден в .env файле")
        return
    
    # Создаем бота
    bot = Bot(token=bot_token)
    
    # Проверяем каждый канал
    results = {}
    campaigns = {}
    
    for channel_key, channel_data in ALL_CHANNELS.items():
        channel_id = channel_data.get('chat_id')
        channel_name = channel_data.get('name', 'Unknown')
        campaign = channel_data.get('campaign', 'default')
        
        if not channel_id:
            print(f"❌ {channel_name}: ID канала не указан")
            continue
        
        print(f"\n📢 Проверка: {channel_name}")
        print(f"   ID: {channel_id}")
        
        result = await check_channel_access(bot, channel_id, channel_name)
        results[channel_key] = result
        
        if result['status'] == 'success':
            print(f"   ✅ Доступен: {result['title']}")
            print(f"   📝 Тип: {result['type']}")
            if result['username']:
                print(f"   🔗 @{result['username']}")
            
            # Группируем по кампаниям
            if campaign not in campaigns:
                campaigns[campaign] = {'success': [], 'error': []}
            campaigns[campaign]['success'].append(channel_name)
        else:
            print(f"   ❌ Ошибка: {result['error']}")
            
            if campaign not in campaigns:
                campaigns[campaign] = {'success': [], 'error': []}
            campaigns[campaign]['error'].append(channel_name)
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    total_success = 0
    total_errors = 0
    
    for campaign, stats in campaigns.items():
        print(f"\n🎯 КАМПАНИЯ: {campaign.upper()}")
        print(f"   ✅ Доступно: {len(stats['success'])}")
        print(f"   ❌ Ошибок: {len(stats['error'])}")
        
        if stats['success']:
            print("   📢 Доступные каналы:")
            for channel in stats['success']:
                print(f"      • {channel}")
        
        if stats['error']:
            print("   ⚠️ Проблемные каналы:")
            for channel in stats['error']:
                print(f"      • {channel}")
        
        total_success += len(stats['success'])
        total_errors += len(stats['error'])
    
    print(f"\n🎉 ОБЩИЙ РЕЗУЛЬТАТ:")
    print(f"   ✅ Доступно: {total_success}")
    print(f"   ❌ Ошибок: {total_errors}")
    
    if total_errors > 0:
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        print("   1. Проверьте, что бот добавлен в каналы как администратор")
        print("   2. Убедитесь, что ID каналов указаны правильно")
        print("   3. Для публичных каналов используйте @username")
        print("   4. Для приватных каналов используйте числовой ID")
    
    # Закрываем бота
    await bot.session.close()
    
    return results

def generate_working_config(results):
    """Генерация рабочей конфигурации"""
    print("\n🔧 ГЕНЕРАЦИЯ РАБОЧЕЙ КОНФИГУРАЦИИ")
    print("=" * 60)
    
    working_channels = {}
    
    for channel_key, result in results.items():
        if result['status'] == 'success':
            original_data = ALL_CHANNELS[channel_key]
            working_channels[channel_key] = {
                'chat_id': str(result['chat_id']),
                'name': result['title'],
                'active': True,
                'campaign': original_data.get('campaign', 'default'),
                'target_audience': original_data.get('target_audience', 'All'),
                'description': original_data.get('description', ''),
                'username': result.get('username', ''),
                'type': result['type']
            }
    
    if working_channels:
        print("✅ Рабочие каналы:")
        for key, data in working_channels.items():
            print(f"   • {data['name']} ({data['chat_id']})")
        
        # Сохраняем в файл
        import json
        with open('working_channels.json', 'w', encoding='utf-8') as f:
            json.dump(working_channels, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Рабочая конфигурация сохранена в working_channels.json")
    else:
        print("❌ Нет рабочих каналов")

async def main():
    """Основная функция"""
    results = await check_all_channels()
    generate_working_config(results)

if __name__ == "__main__":
    asyncio.run(main()) 