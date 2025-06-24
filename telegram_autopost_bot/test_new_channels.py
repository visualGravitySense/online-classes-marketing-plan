#!/usr/bin/env python3
"""
Тестовые посты только в два новых канала
"""

import requests
from datetime import datetime
import time

def send_test_posts_to_new_channels():
    channels = [
        {"id": "@designer_lfe", "title": "Жизнь Дизайнера"},
        {"id": "@digo_online_schools", "title": "Product Design & ML"}
    ]
    print("🚀 ОТПРАВКА ТЕСТОВЫХ ПОСТОВ В НОВЫЕ КАНАЛЫ")
    print("=" * 60)
    
    # Проверяем API сервер через корневой эндпоинт
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API сервер работает")
        else:
            print("❌ API сервер не отвечает")
            return
    except Exception as e:
        print(f"❌ API сервер не запущен: {e}")
        return
    
    for i, channel in enumerate(channels, 1):
        print(f"\n📢 [{i}/2] Отправка в {channel['id']} ({channel['title']})...")
        test_post = {
            "channel_id": channel["id"],
            "content": f"🧪 ТЕСТОВЫЙ ПОСТ ДЛЯ {channel['title']}\n\n📅 Время: {datetime.now().strftime('%H:%M:%S')}\n\n✅ Если вы видите этот пост - бот работает с этим каналом!\n\n🎯 Это тест автоматической публикации.",
            "scheduled_time": datetime.now().isoformat()
        }
        try:
            # Используем правильный путь /api/posts
            response = requests.post(
                "http://localhost:8000/api/posts",
                json=test_post,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                post_data = response.json()
                print(f"✅ Пост создан (ID: {post_data['post_id']})")
                
                # Отправляем тестовый пост через специальный эндпоинт
                test_request = {
                    "channel_id": channel["id"],
                    "content": f"🧪 ТЕСТОВЫЙ ПОСТ ДЛЯ {channel['title']}\n\n📅 Время: {datetime.now().strftime('%H:%M:%S')}\n\n✅ Если вы видите этот пост - бот работает с этим каналом!\n\n🎯 Это тест автоматической публикации."
                }
                
                immediate_response = requests.post(
                    "http://localhost:8000/api/test_post",
                    json=test_request,
                    headers={"Content-Type": "application/json"}
                )
                
                if immediate_response.status_code == 200:
                    print(f"✅ Тестовый пост отправлен в {channel['id']}")
                else:
                    print(f"⚠️ Пост создан, но не отправлен: {immediate_response.text}")
            else:
                print(f"❌ Ошибка создания поста: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка при работе с {channel['id']}: {str(e)}")
        time.sleep(2)
    print("\n" + "=" * 60)
    print("🏁 ТЕСТОВЫЕ ПОСТЫ ОТПРАВЛЕНЫ В НОВЫЕ КАНАЛЫ")
    print("\n💡 Проверьте каналы:")
    for channel in channels:
        print(f"   • {channel['id']} ({channel['title']})")
    print("\n📊 Если посты не пришли - проверьте права бота и логи main.py!")

if __name__ == "__main__":
    send_test_posts_to_new_channels() 