#!/usr/bin/env python3
"""
Скрипт для планирования тестовых постов в Telegram каналах
"""

import requests
import time
from datetime import datetime, timedelta

def schedule_test_posts():
    """Планирует тестовые посты в каналах на 12:40"""
    
    # Время публикации: 12:40
    scheduled_time = datetime.now().replace(hour=12, minute=40, second=0, microsecond=0)
    
    # Если время уже прошло, планируем на завтра
    if scheduled_time < datetime.now():
        scheduled_time += timedelta(days=1)
    
    print(f"⏰ Планирование постов на: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Тестовые каналы с контентом
    channels = [
        {
            'chat_id': '-1002091962525',
            'name': 'digoGraphickDesign',
            'content': """🎨 UX/UI Принцип дня

💡 "Консистентность - ключ к успеху"

Пользователи ожидают, что элементы интерфейса будут вести себя предсказуемо. Консистентность в дизайне создает доверие и улучшает пользовательский опыт.

🔧 Практические советы:
• Используйте единую цветовую палитру
• Соблюдайте одинаковые отступы
• Применяйте единообразные иконки
• Следуйте единому стилю кнопок

📚 Изучайте паттерны дизайна и применяйте их последовательно!

🔖 Сохраняй пост, чтобы не потерять!
💬 Делись своим мнением в комментариях

#UXUITips #Дизайн #Консистентность #UXUI"""
        },
        {
            'chat_id': '-1002123538949',
            'name': 'digoUI',
            'content': """📊 UX/UI Кейс: Мобильное приложение

🎯 Задача: Улучшить навигацию в мобильном приложении

❌ Проблемы в старом дизайне:
- Скрытое меню в боковой панели
- Неочевидная иерархия разделов
- Сложный процесс поиска

✅ Решение:
- Нижняя навигация с 5 основными разделами
- Четкая визуальная иерархия
- Умный поиск с автодополнением

📈 Результат: +45% времени в приложении, -30% отказов

💡 Вывод: Простая навигация = довольные пользователи

❓ Как бы вы улучшили навигацию?
👆 Ставь лайк, если кейс полезен!

#Кейс #UXDesign #МобильныйДизайн #Навигация"""
        }
    ]
    
    print("🚀 ПЛАНИРОВАНИЕ ТЕСТОВЫХ ПОСТОВ В TELEGRAM")
    print("="*50)
    
    for channel in channels:
        print(f"\n📢 Планирование в канал: {channel['name']}")
        
        try:
            # Создаем запланированный пост
            post_data = {
                "content": channel['content'],
                "channel_id": channel['chat_id'],
                "scheduled_time": scheduled_time.isoformat(),
                "media_path": None,
                "media_type": None
            }
            
            response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Пост запланирован в {channel['name']}")
                print(f"📄 ID поста: {result.get('post_id')}")
                print(f"⏰ Время публикации: {scheduled_time.strftime('%H:%M')}")
                print(f"📄 Контент: {channel['content'][:50]}...")
            else:
                print(f"❌ Ошибка планирования: {response.status_code}")
                print(f"📄 Ответ: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Не удалось подключиться к API серверу")
            print("💡 Убедитесь, что API сервер запущен: python api.py")
        except Exception as e:
            print(f"❌ Ошибка планирования в {channel['name']}: {e}")
        
        print("-" * 30)
        time.sleep(1)  # Пауза между запросами

def check_scheduled_posts():
    """Проверяет запланированные посты"""
    print("\n📋 ПРОВЕРКА ЗАПЛАНИРОВАННЫХ ПОСТОВ")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:8000/api/posts", timeout=5)
        if response.status_code == 200:
            posts = response.json()
            
            # Фильтруем запланированные посты
            scheduled_posts = [post for post in posts if not post.get('published', False)]
            
            print(f"📊 Всего постов: {len(posts)}")
            print(f"⏳ Запланировано: {len(scheduled_posts)}")
            
            if scheduled_posts:
                print("\n📝 Запланированные посты:")
                for i, post in enumerate(scheduled_posts[:5], 1):  # Показываем первые 5
                    scheduled_time = post.get('scheduled_time', 'N/A')
                    channel_name = post.get('channel_name', 'N/A')
                    content_preview = post.get('content', '')[:50] + "..."
                    
                    print(f"   {i}. ID: {post.get('id')} | Канал: {channel_name}")
                    print(f"      ⏰ Время: {scheduled_time}")
                    print(f"      📄 Контент: {content_preview}")
                    print()
            else:
                print("📭 Нет запланированных постов")
                
        else:
            print(f"❌ Ошибка получения постов: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка проверки постов: {e}")

def check_api_status():
    """Проверяет статус API"""
    try:
        response = requests.get("http://localhost:8000/api/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API сервер работает")
            print(f"📊 Статистика: {stats.get('total_posts', 0)} постов")
            return True
        else:
            print(f"❌ API сервер недоступен: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API сервер недоступен: {e}")
        return False

if __name__ == "__main__":
    print("🎯 ЗАПУСК ПЛАНИРОВАНИЯ ТЕСТОВЫХ ПОСТОВ")
    print("="*60)
    
    # Проверяем API
    if check_api_status():
        # Планируем посты
        schedule_test_posts()
        
        # Проверяем результат
        check_scheduled_posts()
        
        print("\n💡 Посты запланированы!")
        print("📅 Планировщик автоматически опубликует их в указанное время")
        print("🔍 Проверить статус можно через веб-интерфейс: http://localhost:8000")
    else:
        print("\n💡 Для запуска API сервера выполните:")
        print("   python api.py")
    
    print("\n" + "="*60)
    print("✅ ПЛАНИРОВАНИЕ ЗАВЕРШЕНО!")
    print("="*60) 