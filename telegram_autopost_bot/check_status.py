#!/usr/bin/env python3
"""
Скрипт для проверки статуса системы
"""

import requests
from datetime import datetime

def check_api_health():
    """Проверяет здоровье API"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            return True, "✅ API работает"
        else:
            return False, f"❌ API ошибка: {response.status_code}"
    except Exception as e:
        return False, f"❌ API недоступен: {e}"

def get_channels_status():
    """Получает статус каналов"""
    try:
        response = requests.get("http://localhost:8000/api/channels", timeout=10)
        if response.status_code == 200:
            channels = response.json()
            return True, channels
        else:
            return False, f"Ошибка получения каналов: {response.status_code}"
    except Exception as e:
        return False, f"Ошибка: {e}"

def get_posts_status():
    """Получает статус постов"""
    try:
        response = requests.get("http://localhost:8000/api/posts", timeout=10)
        if response.status_code == 200:
            posts = response.json()
            return True, posts
        else:
            return False, f"Ошибка получения постов: {response.status_code}"
    except Exception as e:
        return False, f"Ошибка: {e}"

def analyze_posts(posts):
    """Анализирует посты"""
    if not posts:
        return "Нет постов"
    
    total = len(posts)
    published = sum(1 for post in posts if post.get('published', False))
    scheduled = total - published
    
    # Группируем по каналам
    channel_stats = {}
    for post in posts:
        channel_id = post.get('channel_id', 'unknown')
        if channel_id not in channel_stats:
            channel_stats[channel_id] = {'total': 0, 'published': 0, 'scheduled': 0}
        
        channel_stats[channel_id]['total'] += 1
        if post.get('published', False):
            channel_stats[channel_id]['published'] += 1
        else:
            channel_stats[channel_id]['scheduled'] += 1
    
    return {
        'total': total,
        'published': published,
        'scheduled': scheduled,
        'channels': channel_stats
    }

def main():
    print("📊 СТАТУС СИСТЕМЫ")
    print("="*60)
    print(f"🕐 Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Проверяем API
    api_ok, api_msg = check_api_health()
    print(f"🔧 API: {api_msg}")
    
    if not api_ok:
        print("\n❌ API недоступен. Запустите сервер командой: python api.py")
        return
    
    print()
    
    # Проверяем каналы
    channels_ok, channels_data = get_channels_status()
    if channels_ok:
        print(f"📢 КАНАЛЫ ({len(channels_data)}):")
        for channel in channels_data:
            status = "✅ Активен" if channel.get('active') else "❌ Неактивен"
            print(f"   • {channel.get('name', 'N/A')}: {status}")
    else:
        print(f"❌ Ошибка каналов: {channels_data}")
    
    print()
    
    # Проверяем посты
    posts_ok, posts_data = get_posts_status()
    if posts_ok:
        analysis = analyze_posts(posts_data)
        print(f"📝 ПОСТЫ:")
        print(f"   • Всего: {analysis['total']}")
        print(f"   • Опубликовано: {analysis['published']}")
        print(f"   • Запланировано: {analysis['scheduled']}")
        
        if analysis['channels']:
            print("\n📊 По каналам:")
            for channel_id, stats in analysis['channels'].items():
                print(f"   • {channel_id}: {stats['total']} постов ({stats['published']} опубл., {stats['scheduled']} запл.)")
    else:
        print(f"❌ Ошибка постов: {posts_data}")
    
    print()
    print("="*60)
    print("✅ Проверка завершена")

if __name__ == "__main__":
    main() 