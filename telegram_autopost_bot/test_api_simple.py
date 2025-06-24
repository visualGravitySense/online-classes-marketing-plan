#!/usr/bin/env python3
"""
Простой тест API
"""

import requests
import json

def test_api():
    """Тестирует API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 ТЕСТИРОВАНИЕ API")
    print("="*50)
    
    # Тест 1: Главная страница
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Главная страница: {response.status_code}")
    except Exception as e:
        print(f"❌ Главная страница: {e}")
    
    # Тест 2: Каналы
    try:
        response = requests.get(f"{base_url}/api/channels", timeout=5)
        if response.status_code == 200:
            channels = response.json()
            print(f"✅ Каналы: {len(channels)} найдено")
            for channel in channels:
                print(f"   • {channel.get('name', 'N/A')} ({channel.get('chat_id', 'N/A')})")
        else:
            print(f"❌ Каналы: {response.status_code}")
    except Exception as e:
        print(f"❌ Каналы: {e}")
    
    # Тест 3: Посты
    try:
        response = requests.get(f"{base_url}/api/posts", timeout=5)
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Посты: {len(posts)} найдено")
        else:
            print(f"❌ Посты: {response.status_code}")
    except Exception as e:
        print(f"❌ Посты: {e}")
    
    # Тест 4: Статистика
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Статистика: получена")
            print(f"   • Каналов: {stats.get('channels', 0)}")
            print(f"   • Постов: {stats.get('posts', 0)}")
        else:
            print(f"❌ Статистика: {response.status_code}")
    except Exception as e:
        print(f"❌ Статистика: {e}")

if __name__ == "__main__":
    test_api() 