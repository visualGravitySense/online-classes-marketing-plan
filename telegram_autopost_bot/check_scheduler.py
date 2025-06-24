#!/usr/bin/env python3
"""
Скрипт для проверки и запуска планировщика постов
"""

import requests
import time
from datetime import datetime

def check_scheduler_status():
    """Проверяет статус планировщика"""
    print("🔍 ПРОВЕРКА СТАТУСА ПЛАНИРОВЩИКА")
    print("="*50)
    
    try:
        # Проверяем API
        response = requests.get("http://localhost:8000/api/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API сервер работает")
            print(f"📊 Статистика: {stats}")
            
            # Проверяем посты
            posts_response = requests.get("http://localhost:8000/api/posts", timeout=5)
            if posts_response.status_code == 200:
                posts = posts_response.json()
                
                # Находим запланированные посты
                scheduled_posts = [post for post in posts if not post.get('published', False)]
                published_posts = [post for post in posts if post.get('published', False)]
                
                print(f"\n📝 Посты:")
                print(f"   • Всего: {len(posts)}")
                print(f"   • Опубликовано: {len(published_posts)}")
                print(f"   • Запланировано: {len(scheduled_posts)}")
                
                if scheduled_posts:
                    print(f"\n⏳ Запланированные посты:")
                    for post in scheduled_posts:
                        scheduled_time = post.get('scheduled_time', 'N/A')
                        channel_name = post.get('channel_name', 'N/A')
                        content_preview = post.get('content', '')[:50] + "..."
                        
                        print(f"   • ID: {post.get('id')} | Канал: {channel_name}")
                        print(f"     ⏰ Время: {scheduled_time}")
                        print(f"     📄 Контент: {content_preview}")
                        print()
                
                return True
            else:
                print(f"❌ Ошибка получения постов: {posts_response.status_code}")
                return False
        else:
            print(f"❌ API сервер недоступен: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")
        return False

def start_scheduler():
    """Запускает планировщик"""
    print("\n🚀 ЗАПУСК ПЛАНИРОВЩИКА")
    print("="*50)
    
    try:
        response = requests.post("http://localhost:8000/api/scheduler/start", timeout=5)
        if response.status_code == 200:
            print("✅ Планировщик запущен")
            return True
        else:
            print(f"❌ Ошибка запуска планировщика: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска планировщика: {e}")
        return False

def send_manual_test_post():
    """Отправляет тестовый пост вручную"""
    print("\n📤 ОТПРАВКА ТЕСТОВОГО ПОСТА ВРУЧНУЮ")
    print("="*50)
    
    test_content = """🧪 ТЕСТОВЫЙ ПОСТ

Это тестовый пост для проверки работы бота.

⏰ Время отправки: {time}

✅ Если вы видите этот пост, значит бот работает!

#Тест #UXUI #Бот""".format(time=datetime.now().strftime('%H:%M:%S'))
    
    channels = [
        {'chat_id': '-1002091962525', 'name': 'digoGraphickDesign'},
        {'chat_id': '-1002123538949', 'name': 'digoUI'}
    ]
    
    for channel in channels:
        print(f"\n📢 Отправка в {channel['name']}...")
        
        try:
            test_data = {
                "channel_id": channel['chat_id'],
                "content": test_content
            }
            
            response = requests.post("http://localhost:8000/api/test_post", json=test_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Тестовый пост отправлен в {channel['name']}")
            else:
                print(f"❌ Ошибка отправки: {response.status_code}")
                print(f"📄 Ответ: {response.text}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки в {channel['name']}: {e}")

def check_bot_token():
    """Проверяет настройки бота"""
    print("\n🤖 ПРОВЕРКА НАСТРОЕК БОТА")
    print("="*50)
    
    try:
        from config import BOT_TOKEN, ADMIN_ID
        
        if BOT_TOKEN and BOT_TOKEN != "your_bot_token_here":
            print(f"✅ Токен бота настроен: {BOT_TOKEN[:10]}...")
        else:
            print("❌ Токен бота не настроен!")
            print("💡 Создайте файл .env с BOT_TOKEN=ваш_токен")
        
        if ADMIN_ID and ADMIN_ID != 0:
            print(f"✅ ID администратора: {ADMIN_ID}")
        else:
            print("❌ ID администратора не настроен!")
            print("💡 Добавьте ADMIN_ID=ваш_id в .env")
            
    except Exception as e:
        print(f"❌ Ошибка проверки настроек: {e}")

if __name__ == "__main__":
    print("🔧 ДИАГНОСТИКА ПЛАНИРОВЩИКА")
    print("="*60)
    
    # Проверяем настройки бота
    check_bot_token()
    
    # Проверяем статус
    if check_scheduler_status():
        # Запускаем планировщик
        if start_scheduler():
            print("\n💡 Планировщик запущен!")
            print("⏳ Запланированные посты будут опубликованы автоматически")
            
            # Отправляем тестовый пост
            send_manual_test_post()
        else:
            print("\n❌ Не удалось запустить планировщик")
    else:
        print("\n❌ Проблемы с API сервером")
        print("💡 Убедитесь, что API сервер запущен: python api.py")
    
    print("\n" + "="*60)
    print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА!")
    print("="*60) 