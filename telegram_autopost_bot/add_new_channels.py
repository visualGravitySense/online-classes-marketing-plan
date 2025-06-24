#!/usr/bin/env python3
"""
Скрипт для добавления новых каналов и создания постов
"""

import requests
import time
from datetime import datetime, timedelta
from integrated_content_generator import ContentGenerator

def add_new_channels():
    """Добавляет новые каналы в систему"""
    
    print("📢 ДОБАВЛЕНИЕ НОВЫХ КАНАЛОВ")
    print("="*50)
    
    # Новые каналы
    new_channels = [
        {
            'name': 'digo_online_schools',
            'chat_id': '-1002316535443',
            'description': 'Product Design & ML - Разработка продукта для услуг на основе машинного обучения'
        },
        {
            'name': 'designer_lfe',
            'chat_id': '-1001903756368',
            'description': 'Жизнь Дизайнера'
        }
    ]
    
    for channel in new_channels:
        print(f"\n📢 Добавление канала: {channel['name']}")
        print(f"   ID: {channel['chat_id']}")
        print(f"   Описание: {channel['description']}")
        
        try:
            # Добавляем канал через API
            channel_data = {
                "name": channel['name'],
                "chat_id": channel['chat_id'],
                "active": True
            }
            
            response = requests.post("http://localhost:8000/api/channels", json=channel_data, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Канал {channel['name']} добавлен успешно")
            else:
                print(f"   ❌ Ошибка добавления: {response.status_code}")
                print(f"   📄 Ответ: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        print("-" * 30)

def create_posts_for_new_channels():
    """Создает посты для новых каналов"""
    
    print("\n📝 СОЗДАНИЕ ПОСТОВ ДЛЯ НОВЫХ КАНАЛОВ")
    print("="*50)
    
    # Специальный контент для новых каналов
    channel_content = {
        'digo_online_schools': {
            'chat_id': '-1002316535443',
            'name': 'digo_online_schools',
            'posts': [
                {
                    'content': """🤖 Product Design & ML

💡 Как машинное обучение меняет дизайн продуктов

Сегодня ML-алгоритмы помогают дизайнерам создавать более персонализированные интерфейсы и предсказывать поведение пользователей.

🔧 Практические применения:
• Персонализация контента
• A/B тестирование с ML
• Предсказание конверсии
• Автоматическая оптимизация

📊 Результат: +40% вовлеченности пользователей

🎯 Готовы изучать ML для дизайна?

#ProductDesign #MachineLearning #UXDesign #ML""",
                    'scheduled_time': datetime.now() + timedelta(hours=1)
                },
                {
                    'content': """📊 Кейс: ML в E-commerce

🎯 Задача: Увеличить продажи на 30% с помощью персонализации

❌ Проблемы:
- Статичные рекомендации
- Низкая конверсия
- Высокий отток пользователей

✅ ML-решение:
- Персональные рекомендации
- Динамическое ценообразование
- Предсказание оттока

📈 Результат: +45% продаж, -25% оттока

💡 ML + UX = Супер результат!

#ML #Ecommerce #UXDesign #Кейс""",
                    'scheduled_time': datetime.now() + timedelta(hours=3)
                }
            ]
        },
        'designer_lfe': {
            'chat_id': '-1001903756368',
            'name': 'designer_lfe',
            'posts': [
                {
                    'content': """🎨 Жизнь Дизайнера

💼 Как построить успешную карьеру в дизайне

Дизайн - это не только про красоту, но и про решение бизнес-задач. Успешный дизайнер понимает потребности пользователей и бизнеса.

🚀 Ключевые навыки:
• UX/UI дизайн
• Работа с данными
• Коммуникация с заказчиками
• Постоянное обучение

💡 Совет: Изучайте не только дизайн, но и бизнес-процессы

📈 Результат: Стабильный доход и интересные проекты

#Дизайн #Карьера #UXUI #ЖизньДизайнера""",
                    'scheduled_time': datetime.now() + timedelta(hours=2)
                },
                {
                    'content': """🔥 Дизайн-мышление в жизни

🧠 Как применять принципы дизайна в повседневных задачах

Дизайн-мышление - это не только для работы. Эти принципы помогают решать любые проблемы:

1️⃣ Эмпатия - понимание потребностей
2️⃣ Фокусировка - определение проблемы
3️⃣ Генерация идей - поиск решений
4️⃣ Прототипирование - тестирование
5️⃣ Тестирование - валидация

💡 Попробуйте применить к любой задаче!

🎯 Результат: Более эффективное решение проблем

#ДизайнМышление #Проблемы #Решение #UX""",
                    'scheduled_time': datetime.now() + timedelta(hours=4)
                }
            ]
        }
    }
    
    total_posts = 0
    
    for channel_key, channel_info in channel_content.items():
        print(f"\n📢 Канал: {channel_info['name']}")
        
        for i, post_info in enumerate(channel_info['posts'], 1):
            print(f"   📝 Пост #{i}: {post_info['scheduled_time'].strftime('%H:%M')}")
            
            try:
                post_data = {
                    "content": post_info['content'],
                    "channel_id": channel_info['chat_id'],
                    "scheduled_time": post_info['scheduled_time'].isoformat(),
                    "media_path": None,
                    "media_type": None
                }
                
                response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"      ✅ Пост создан (ID: {result.get('post_id')})")
                    total_posts += 1
                else:
                    print(f"      ❌ Ошибка создания: {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ Ошибка: {e}")
            
            time.sleep(0.5)
        
        print("-" * 30)
    
    return total_posts

def check_all_channels():
    """Проверяет все каналы"""
    print("\n📊 ПРОВЕРКА ВСЕХ КАНАЛОВ")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:8000/api/channels", timeout=5)
        if response.status_code == 200:
            channels = response.json()
            print(f"📢 Всего каналов: {len(channels)}")
            
            for channel in channels:
                status = "✅ Активен" if channel.get('active') else "❌ Неактивен"
                print(f"   • {channel.get('name', 'N/A')}: {status}")
                
        else:
            print(f"❌ Ошибка получения каналов: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    print("🚀 ДОБАВЛЕНИЕ НОВЫХ КАНАЛОВ")
    print("="*60)
    
    try:
        # Добавляем новые каналы
        add_new_channels()
        
        # Создаем специальные посты
        special_posts = create_posts_for_new_channels()
        
        # Проверяем результат
        check_all_channels()
        
        print("\n" + "="*60)
        print("✅ НОВЫЕ КАНАЛЫ ДОБАВЛЕНЫ!")
        print("="*60)
        print(f"📊 Создано постов: {special_posts}")
        print("\n📢 Новые каналы:")
        print("   • @digo_online_schools (Product Design & ML)")
        print("   • @designer_lfe (Жизнь Дизайнера)")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 