#!/usr/bin/env python3
"""
Планирование постов во все каналы с немедленной публикацией
"""

import requests
from datetime import datetime, timedelta
import time

def schedule_immediate_posts():
    """Планируем посты во все каналы с немедленной публикацией"""
    
    print("🚀 ПЛАНИРОВАНИЕ ПОСТОВ ВО ВСЕ КАНАЛЫ")
    print("=" * 60)
    
    # Список всех каналов
    channels = [
        {"id": "@gr de", "title": "Графические дизайнеры", "audience": "Freelancers"},
        {"id": "@ui de", "title": "UX/UI дизайнеры", "audience": "Juniors"},
        {"id": "@digo_online_schools", "title": "Product Design & ML", "audience": "Developers"},
        {"id": "@designer_lfe", "title": "Жизнь Дизайнера", "audience": "Designers"}
    ]
    
    # Проверяем API сервер
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
    
    # Планируем посты в каждый канал
    for i, channel in enumerate(channels, 1):
        print(f"\n📢 [{i}/{len(channels)}] Планирование поста в {channel['id']} ({channel['title']})...")
        
        # Время публикации - через 2 минуты от текущего времени
        publish_time = datetime.now() + timedelta(minutes=2)
        
        # Создаем контент для каждого канала
        content = f"🎯 ПЛАНИРОВАННЫЙ ПОСТ ДЛЯ {channel['audience'].upper()}\n\n"
        content += f"📅 Время публикации: {publish_time.strftime('%H:%M')}\n"
        content += f"📢 Канал: {channel['title']}\n\n"
        content += f"💡 Это тест планировщика для аудитории: {channel['audience']}\n"
        content += "✅ Если вы видите этот пост - планировщик работает!\n\n"
        content += "🚀 Автоматическая публикация работает корректно!"
        
        # Создаем пост через API
        post_data = {
            "channel_id": channel["id"],
            "content": content,
            "scheduled_time": publish_time.isoformat()
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/api/posts",
                json=post_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Пост запланирован (ID: {result['post_id']})")
                print(f"⏰ Время публикации: {publish_time.strftime('%H:%M:%S')}")
            else:
                print(f"❌ Ошибка планирования поста: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка при планировании поста в {channel['id']}: {str(e)}")
        
        # Небольшая пауза между запросами
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🏁 ПОСТЫ ЗАПЛАНИРОВАНЫ ВО ВСЕ КАНАЛЫ")
    print(f"⏰ Все посты будут опубликованы в {publish_time.strftime('%H:%M')}")
    print("\n💡 Проверьте каналы через 2 минуты:")
    for channel in channels:
        print(f"   • {channel['id']} ({channel['title']})")
    
    print("\n📊 Планировщик должен автоматически опубликовать все посты!")
    print("🔍 Если посты не появятся - проверьте логи планировщика")

if __name__ == "__main__":
    schedule_immediate_posts() 