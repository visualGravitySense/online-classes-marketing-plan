#!/usr/bin/env python3
"""
Тест исправленного планировщика постов
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_scheduler():
    """Тестируем исправленный планировщик"""
    
    print("🔧 ТЕСТ ИСПРАВЛЕННОГО ПЛАНИРОВЩИКА")
    print("=" * 50)
    
    # 1. Проверяем статус API
    try:
        response = requests.get("http://localhost:8000/status")
        if response.status_code == 200:
            print("✅ API сервер работает")
        else:
            print("❌ API сервер не отвечает")
            return
    except:
        print("❌ API сервер не запущен")
        return
    
    # 2. Создаем тестовый пост на ближайшее время
    test_time = datetime.now() + timedelta(minutes=2)  # Через 2 минуты
    
    test_post = {
        "channel_id": "@digo_online_schools",
        "content": f"🧪 ТЕСТ ПЛАНИРОВЩИКА\n\nЭтот пост должен быть опубликован автоматически в {test_time.strftime('%H:%M')}\n\n✅ Если вы видите этот пост - планировщик работает!",
        "scheduled_time": test_time.isoformat()
    }
    
    print(f"📝 Создаем тестовый пост на {test_time.strftime('%H:%M')}")
    
    try:
        response = requests.post(
            "http://localhost:8000/posts",
            json=test_post,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            post_data = response.json()
            print(f"✅ Тестовый пост создан (ID: {post_data['id']})")
        else:
            print(f"❌ Ошибка создания поста: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Ошибка при создании поста: {str(e)}")
        return
    
    # 3. Проверяем, что пост в базе
    print("\n📊 Проверяем базу данных...")
    try:
        response = requests.get("http://localhost:8000/posts/pending")
        if response.status_code == 200:
            posts = response.json()
            test_posts = [p for p in posts if "ТЕСТ ПЛАНИРОВЩИКА" in p['content']]
            if test_posts:
                print(f"✅ Тестовый пост найден в базе (ID: {test_posts[0]['id']})")
            else:
                print("❌ Тестовый пост не найден в базе")
        else:
            print(f"❌ Ошибка получения постов: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при проверке базы: {str(e)}")
    
    # 4. Ждем публикации
    print(f"\n⏳ Ждем автоматической публикации в {test_time.strftime('%H:%M')}...")
    print("💡 Проверьте канал @digo_online_schools через 2 минуты")
    
    # 5. Проверяем статус через 3 минуты
    print("\n⏰ Проверяем статус через 3 минуты...")
    time.sleep(180)
    
    try:
        response = requests.get("http://localhost:8000/posts/published")
        if response.status_code == 200:
            posts = response.json()
            test_posts = [p for p in posts if "ТЕСТ ПЛАНИРОВЩИКА" in p['content']]
            if test_posts:
                print("✅ Тестовый пост был опубликован автоматически!")
                print(f"📅 Время публикации: {test_posts[0]['published_time']}")
            else:
                print("❌ Тестовый пост не был опубликован автоматически")
        else:
            print(f"❌ Ошибка проверки опубликованных постов: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при проверке: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 ТЕСТ ЗАВЕРШЕН")

if __name__ == "__main__":
    test_scheduler() 