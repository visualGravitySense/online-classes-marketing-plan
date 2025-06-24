#!/usr/bin/env python3
"""
Тестовые посты во все каналы
"""

import requests
import json
from datetime import datetime, timedelta
import time

def send_test_posts_to_all_channels():
    """Отправляем тестовые посты во все каналы"""
    
    print("🚀 ОТПРАВКА ТЕСТОВЫХ ПОСТОВ ВО ВСЕ КАНАЛЫ")
    print("=" * 60)
    
    # Список всех каналов
    channels = [
        "@gr de",           # Графические дизайнеры
        "@ui de",           # UX/UI дизайнеры
        "@digo_online_schools",  # Product Design & ML
        "@designer_lfe"     # Жизнь дизайнера
    ]
    
    # Проверяем API сервер
    try:
        response = requests.get("http://localhost:8000/status")
        if response.status_code != 200:
            print("❌ API сервер не отвечает")
            return
        print("✅ API сервер работает")
    except:
        print("❌ API сервер не запущен")
        return
    
    # Отправляем тестовые посты в каждый канал
    for i, channel in enumerate(channels, 1):
        print(f"\n📢 [{i}/{len(channels)}] Отправка в {channel}...")
        
        # Создаем тестовый пост
        test_post = {
            "channel_id": channel,
            "content": f"🧪 ТЕСТОВЫЙ ПОСТ #{i}\n\n📅 Время: {datetime.now().strftime('%H:%M:%S')}\n📢 Канал: {channel}\n\n✅ Если вы видите этот пост - бот работает с этим каналом!\n\n🎯 Это тест автоматической публикации.",
            "scheduled_time": datetime.now().isoformat()
        }
        
        try:
            # Отправляем пост через API
            response = requests.post(
                "http://localhost:8000/posts",
                json=test_post,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                post_data = response.json()
                print(f"✅ Пост создан (ID: {post_data['id']})")
                
                # Пытаемся отправить немедленно
                immediate_response = requests.post(
                    f"http://localhost:8000/posts/{post_data['id']}/publish",
                    headers={"Content-Type": "application/json"}
                )
                
                if immediate_response.status_code == 200:
                    print(f"✅ Пост отправлен в {channel}")
                else:
                    print(f"⚠️ Пост создан, но не отправлен: {immediate_response.text}")
                    
            else:
                print(f"❌ Ошибка создания поста: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка при работе с {channel}: {str(e)}")
        
        # Небольшая пауза между постами
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("🏁 ТЕСТОВЫЕ ПОСТЫ ОТПРАВЛЕНЫ ВО ВСЕ КАНАЛЫ")
    print("\n💡 Проверьте каналы:")
    for channel in channels:
        print(f"   • {channel}")
    
    print("\n📊 Если какие-то посты не пришли - проверьте:")
    print("   • Бот добавлен как администратор в канал")
    print("   • У бота есть права на публикацию сообщений")
    print("   • Правильно указан username канала")

if __name__ == "__main__":
    send_test_posts_to_all_channels() 