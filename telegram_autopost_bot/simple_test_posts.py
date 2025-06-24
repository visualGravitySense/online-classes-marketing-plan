#!/usr/bin/env python3
"""
Простой скрипт для тестовых публикаций в Telegram
"""

import requests
import time
from datetime import datetime

def send_test_posts():
    """Отправляет тестовые посты в каналы"""
    
    # Ждем запуска API
    print("⏳ Ожидание запуска API сервера...")
    time.sleep(3)
    
    # Тестовые каналы
    channels = [
        {
            'chat_id': '-1002091962525',
            'name': 'digoGraphickDesign',
            'content': """🎨 UX/UI Совет дня

🔥 Главный принцип дизайна: "Меньше значит больше"

Помните: пользователи приходят за решением, а не за красивой картинкой. Каждый элемент интерфейса должен иметь цель.

💡 Практический совет:
- Убирайте лишние элементы
- Фокусируйтесь на главном действии
- Используйте белое пространство

🔖 Сохраняй пост, чтобы не потерять!
💬 Делись своим мнением в комментариях

#UXUITips #Дизайн #Обучение #UXUI"""
        },
        {
            'chat_id': '-1002123538949',
            'name': 'digoUI',
            'content': """📊 Разбор интерфейса: E-commerce

🎯 Задача: Увеличить конверсию корзины на 25%

❌ Проблемы в старом дизайне:
- Скрытая кнопка "Купить"
- Сложный процесс оформления
- Неочевидная доставка

✅ Решение:
- Кнопка "Купить" на 40% больше
- Упрощенная форма заказа
- Прозрачная информация о доставке

📈 Результат: +32% конверсии за 2 недели

❓ Как бы вы решили эту задачу?
👆 Ставь лайк, если пост полезен!

#Кейс #UXDesign #Интерфейс #Ecommerce"""
        }
    ]
    
    print("🚀 ОТПРАВКА ТЕСТОВЫХ ПОСТОВ В TELEGRAM")
    print("="*50)
    
    for channel in channels:
        print(f"\n📢 Отправка в канал: {channel['name']}")
        
        try:
            # Отправляем тестовый пост
            test_data = {
                "channel_id": channel['chat_id'],
                "content": channel['content']
            }
            
            response = requests.post("http://localhost:8000/api/test_post", json=test_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Тестовый пост отправлен в {channel['name']}")
                print(f"📄 Контент: {channel['content'][:50]}...")
            else:
                print(f"❌ Ошибка отправки: {response.status_code}")
                print(f"📄 Ответ: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Не удалось подключиться к API серверу")
            print("💡 Убедитесь, что API сервер запущен: python api.py")
        except Exception as e:
            print(f"❌ Ошибка отправки в {channel['name']}: {e}")
        
        print("-" * 30)
        time.sleep(2)  # Пауза между отправками

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
    print("🎯 ЗАПУСК ТЕСТОВЫХ ПУБЛИКАЦИЙ")
    print("="*60)
    
    # Проверяем API
    if check_api_status():
        send_test_posts()
    else:
        print("\n💡 Для запуска API сервера выполните:")
        print("   python api.py")
    
    print("\n" + "="*60)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("="*60) 