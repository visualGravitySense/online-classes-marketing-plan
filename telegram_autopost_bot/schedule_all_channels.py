#!/usr/bin/env python3
"""
Скрипт для автоматического расписания постов во всех каналах
"""

import requests
import time
from datetime import datetime, timedelta
from integrated_content_generator import ContentGenerator

def get_all_channels():
    """Получает список всех каналов"""
    try:
        response = requests.get("http://localhost:8000/api/channels", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Ошибка получения каналов: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def schedule_posts_for_week():
    """Создает расписание постов на неделю для всех каналов"""
    
    print("📅 СОЗДАНИЕ РАСПИСАНИЯ НА НЕДЕЛЮ")
    print("="*60)
    
    # Получаем все каналы
    channels = get_all_channels()
    if not channels:
        print("❌ Не удалось получить список каналов")
        return
    
    print(f"📢 Найдено каналов: {len(channels)}")
    
    # Расписание времени публикаций
    schedule_times = {
        'monday': ['09:00', '14:00', '18:00'],
        'tuesday': ['10:00', '15:00', '19:00'],
        'wednesday': ['09:30', '14:30', '18:30'],
        'thursday': ['09:00', '14:00', '18:00'],
        'friday': ['10:00', '15:00', '19:00'],
        'saturday': ['11:00', '16:00'],
        'sunday': ['12:00', '17:00']
    }
    
    # Специальные настройки для разных каналов
    channel_configs = {
        'digo_online_schools': {
            'audience': 'Разработчики',
            'content_types': ['Кейс', 'Совет'],
            'themes': ['ML в дизайне', 'Product Design', 'AI инструменты']
        },
        'designer_lfe': {
            'audience': 'Фрилансеры',
            'content_types': ['Совет', 'Кейс'],
            'themes': ['Карьера дизайнера', 'Дизайн-мышление', 'Бизнес в дизайне']
        },
        'digoGraphickDesign': {
            'audience': 'Новички',
            'content_types': ['Совет', 'Обучение'],
            'themes': ['Основы дизайна', 'Цвета и типографика', 'Композиция']
        },
        'digoUI': {
            'audience': 'Джуниоры',
            'content_types': ['Кейс', 'Совет'],
            'themes': ['UI компоненты', 'UX принципы', 'Прототипирование']
        }
    }
    
    generator = ContentGenerator()
    total_posts = 0
    
    # Начинаем с завтрашнего дня
    start_date = datetime.now() + timedelta(days=1)
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    for day_name, times in schedule_times.items():
        print(f"\n📅 {day_name.upper()}")
        print("-" * 40)
        
        # Вычисляем дату для этого дня недели
        days_ahead = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        target_date = start_date + timedelta(days=days_ahead[day_name])
        
        for time_str in times:
            print(f"   ⏰ {time_str}")
            
            # Парсим время
            hour, minute = map(int, time_str.split(':'))
            post_time = target_date.replace(hour=hour, minute=minute)
            
            # Создаем посты для каждого канала
            for channel in channels:
                channel_name = channel.get('name', 'unknown')
                chat_id = channel.get('chat_id')
                
                if not chat_id:
                    continue
                
                # Получаем конфигурацию для канала
                config = channel_configs.get(channel_name, {
                    'audience': 'Новички',
                    'content_types': ['Совет'],
                    'themes': ['UX/UI дизайн']
                })
                
                # Выбираем тип контента
                content_type = config['content_types'][total_posts % len(config['content_types'])]
                
                try:
                    # Генерируем контент
                    content = generator.generate_content(
                        config['audience'],
                        content_type
                    )
                    
                    # Создаем пост
                    post_data = {
                        "content": content,
                        "channel_id": chat_id,
                        "scheduled_time": post_time.isoformat(),
                        "media_path": None,
                        "media_type": None
                    }
                    
                    response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"      ✅ {channel_name}: {content_type} (ID: {result.get('post_id')})")
                        total_posts += 1
                    else:
                        print(f"      ❌ {channel_name}: ошибка {response.status_code}")
                        
                except Exception as e:
                    print(f"      ❌ {channel_name}: {e}")
                
                time.sleep(0.5)  # Небольшая пауза между запросами
            
            print()
    
    return total_posts

def create_special_posts():
    """Создает специальные посты для новых каналов"""
    
    print("\n🎯 СОЗДАНИЕ СПЕЦИАЛЬНЫХ ПОСТОВ")
    print("="*50)
    
    special_posts = [
        {
            'channel_id': '-1002316535443',  # digo_online_schools
            'content': """🚀 НОВЫЙ КАНАЛ: Product Design & ML

🤖 Добро пожаловать в мир, где дизайн встречается с машинным обучением!

💡 Здесь мы изучаем:
• Как ML меняет дизайн продуктов
• Персонализация интерфейсов
• AI-инструменты для дизайнеров
• Кейсы успешных проектов

📊 Каждый день - новые знания и практические советы

🎯 Готовы стать экспертом в Product Design & ML?

#ProductDesign #MachineLearning #UXDesign #НовыйКанал""",
            'scheduled_time': datetime.now() + timedelta(hours=1)
        },
        {
            'channel_id': '-1001903756368',  # designer_lfe
            'content': """🎨 НОВЫЙ КАНАЛ: Жизнь Дизайнера

💼 Добро пожаловать в сообщество дизайнеров!

🔥 Здесь мы обсуждаем:
• Карьерный рост в дизайне
• Дизайн-мышление в жизни
• Бизнес-аспекты дизайна
• Вдохновение и креативность

💡 Каждый пост - шаг к успешной карьере

🎯 Готовы развиваться вместе?

#ЖизньДизайнера #Карьера #UXUI #НовыйКанал""",
            'scheduled_time': datetime.now() + timedelta(hours=2)
        }
    ]
    
    total_special = 0
    
    for post_info in special_posts:
        try:
            post_data = {
                "content": post_info['content'],
                "channel_id": post_info['channel_id'],
                "scheduled_time": post_info['scheduled_time'].isoformat(),
                "media_path": None,
                "media_type": None
            }
            
            response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Специальный пост создан (ID: {result.get('post_id')})")
                total_special += 1
            else:
                print(f"❌ Ошибка создания специального поста: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    return total_special

def check_scheduled_posts():
    """Проверяет запланированные посты"""
    print("\n📊 ПРОВЕРКА ЗАПЛАНИРОВАННЫХ ПОСТОВ")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:8000/api/posts", timeout=10)
        if response.status_code == 200:
            posts = response.json()
            
            # Группируем по каналам
            channel_posts = {}
            for post in posts:
                channel_id = post.get('channel_id')
                if channel_id not in channel_posts:
                    channel_posts[channel_id] = 0
                channel_posts[channel_id] += 1
            
            print(f"📝 Всего постов: {len(posts)}")
            print("\n📢 По каналам:")
            for channel_id, count in channel_posts.items():
                print(f"   • {channel_id}: {count} постов")
                
        else:
            print(f"❌ Ошибка получения постов: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    print("🚀 АВТОМАТИЧЕСКОЕ РАСПИСАНИЕ ВСЕХ КАНАЛОВ")
    print("="*70)
    
    try:
        # Создаем специальные посты
        special_posts = create_special_posts()
        
        # Создаем расписание на неделю
        weekly_posts = schedule_posts_for_week()
        
        # Проверяем результат
        check_scheduled_posts()
        
        print("\n" + "="*70)
        print("✅ РАСПИСАНИЕ СОЗДАНО!")
        print("="*70)
        print(f"📊 Создано постов:")
        print(f"   • Специальных: {special_posts}")
        print(f"   • На неделю: {weekly_posts}")
        print(f"   • Всего: {special_posts + weekly_posts}")
        print("\n📢 Каналы в системе:")
        channels = get_all_channels()
        for channel in channels:
            print(f"   • {channel.get('name', 'N/A')} ({channel.get('chat_id', 'N/A')})")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 