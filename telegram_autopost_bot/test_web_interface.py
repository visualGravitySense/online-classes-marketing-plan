#!/usr/bin/env python3
"""
Тестовый скрипт для проверки веб-интерфейса
"""

import requests
import json
from datetime import datetime, timedelta

def test_api_endpoints():
    """Тестирует API эндпоинты"""
    print("🌐 Тестирование API эндпоинтов...")
    
    base_url = "http://localhost:8000"
    
    # Тестируем статистику
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ /api/stats - работает")
            print(f"   • Всего постов: {stats.get('total_posts', 0)}")
            print(f"   • Опубликовано: {stats.get('published_posts', 0)}")
            print(f"   • Активных каналов: {stats.get('active_channels', 0)}")
        else:
            print(f"❌ /api/stats - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ /api/stats - не удалось подключиться: {e}")
    
    # Тестируем получение каналов
    try:
        response = requests.get(f"{base_url}/api/channels")
        if response.status_code == 200:
            channels = response.json()
            print(f"✅ /api/channels - работает, каналов: {len(channels)}")
        else:
            print(f"❌ /api/channels - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ /api/channels - не удалось подключиться: {e}")
    
    # Тестируем получение постов
    try:
        response = requests.get(f"{base_url}/api/posts")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ /api/posts - работает, постов: {len(posts)}")
        else:
            print(f"❌ /api/posts - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ /api/posts - не удалось подключиться: {e}")
    
    # Тестируем аудитории
    try:
        response = requests.get(f"{base_url}/api/content/audiences")
        if response.status_code == 200:
            audiences = response.json()
            print(f"✅ /api/content/audiences - работает")
            print(f"   • Доступные аудитории: {', '.join(audiences.get('audiences', []))}")
        else:
            print(f"❌ /api/content/audiences - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ /api/content/audiences - не удалось подключиться: {e}")
    
    # Тестируем типы контента
    try:
        response = requests.get(f"{base_url}/api/content/types")
        if response.status_code == 200:
            content_types = response.json()
            print(f"✅ /api/content/types - работает")
            print(f"   • Типы контента: {', '.join(content_types.get('content_types', []))}")
        else:
            print(f"❌ /api/content/types - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ /api/content/types - не удалось подключиться: {e}")

def test_content_generation():
    """Тестирует генерацию контента через API"""
    print("\n🎯 Тестирование генерации контента через API...")
    
    base_url = "http://localhost:8000"
    
    # Тестируем генерацию контента
    try:
        data = {
            "audience_group": "Новички в дизайне",
            "content_type": "Совет",
            "channel_id": "-1001234567890",
            "custom_prompt": None
        }
        
        response = requests.post(f"{base_url}/api/content/generate", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Генерация контента работает")
            print(f"   • Preview ID: {result.get('preview_id')}")
            print(f"   • Контент: {result.get('content', '')[:100]}...")
        else:
            print(f"❌ Генерация контента - ошибка {response.status_code}")
            print(f"   • Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Генерация контента - не удалось подключиться: {e}")

def test_post_creation():
    """Тестирует создание постов через API"""
    print("\n📝 Тестирование создания постов через API...")
    
    base_url = "http://localhost:8000"
    
    # Сначала добавляем канал
    try:
        channel_data = {
            "name": "Test Channel API",
            "chat_id": "-1001234567890",
            "active": True
        }
        
        response = requests.post(f"{base_url}/api/channels", json=channel_data)
        if response.status_code == 200:
            print("✅ Канал добавлен через API")
        else:
            print(f"❌ Добавление канала - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ Добавление канала - не удалось подключиться: {e}")
    
    # Тестируем создание поста
    try:
        post_data = {
            "content": "Тестовый пост через API",
            "channel_id": "-1001234567890",
            "scheduled_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "media_path": None,
            "media_type": None
        }
        
        response = requests.post(f"{base_url}/api/posts", json=post_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Создание поста работает")
            print(f"   • Post ID: {result.get('post_id')}")
        else:
            print(f"❌ Создание поста - ошибка {response.status_code}")
            print(f"   • Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Создание поста - не удалось подключиться: {e}")

def test_analytics():
    """Тестирует аналитику контента"""
    print("\n📊 Тестирование аналитики контента...")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/api/content/analytics")
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Аналитика контента работает")
            print(f"   • Всего постов: {analytics.get('total_posts', 0)}")
            print(f"   • Опубликовано: {analytics.get('published_posts', 0)}")
            print(f"   • Ошибок: {analytics.get('failed_posts', 0)}")
            print(f"   • Успешность: {analytics.get('success_rate', 0):.1f}%")
        else:
            print(f"❌ Аналитика контента - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ Аналитика контента - не удалось подключиться: {e}")

def test_main_page():
    """Тестирует главную страницу"""
    print("\n🏠 Тестирование главной страницы...")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Главная страница доступна")
            print(f"   • Размер ответа: {len(response.text)} символов")
        else:
            print(f"❌ Главная страница - ошибка {response.status_code}")
    except Exception as e:
        print(f"❌ Главная страница - не удалось подключиться: {e}")

if __name__ == "__main__":
    print("🌐 ЗАПУСК ТЕСТИРОВАНИЯ ВЕБ-ИНТЕРФЕЙСА")
    print("="*60)
    
    try:
        test_api_endpoints()
        test_content_generation()
        test_post_creation()
        test_analytics()
        test_main_page()
        
        print("\n" + "="*60)
        print("✅ ТЕСТИРОВАНИЕ ВЕБ-ИНТЕРФЕЙСА ЗАВЕРШЕНО!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 