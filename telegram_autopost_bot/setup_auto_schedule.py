#!/usr/bin/env python3
"""
Скрипт для настройки автоматического расписания публикаций
"""

import requests
import time
from datetime import datetime, timedelta
from integrated_content_generator import ContentGenerator

def setup_auto_schedule():
    """Настраивает автоматическое расписание публикаций"""
    
    print("📅 НАСТРОЙКА АВТОМАТИЧЕСКОГО РАСПИСАНИЯ")
    print("="*60)
    
    # Расписание публикаций (время в формате ЧЧ:ММ)
    schedule = {
        'monday': ['09:00', '14:00', '18:00'],
        'tuesday': ['10:00', '15:00', '19:00'],
        'wednesday': ['09:30', '14:30', '18:30'],
        'thursday': ['09:00', '14:00', '18:00'],
        'friday': ['10:00', '15:00', '19:00'],
        'saturday': ['11:00', '16:00'],
        'sunday': ['12:00', '17:00']
    }
    
    # Каналы для публикаций
    channels = [
        {'chat_id': '-1002091962525', 'name': 'digoGraphickDesign'},
        {'chat_id': '-1002123538949', 'name': 'digoUI'}
    ]
    
    # Аудитории и типы контента
    audiences = ["Новички в дизайне", "Junior дизайнеры", "Фрилансеры", "Разработчики"]
    content_types = ["Проблема", "Решение", "Преимущества курса", "Кейс", "Совет", "Мотивация"]
    
    # Создаем генератор контента
    generator = ContentGenerator()
    
    print(f"📊 Настройка расписания:")
    print(f"   • Дней в неделю: {len(schedule)}")
    print(f"   • Каналов: {len(channels)}")
    print(f"   • Аудиторий: {len(audiences)}")
    print(f"   • Типов контента: {len(content_types)}")
    
    # Планируем посты на следующие 7 дней
    total_posts = 0
    
    for day_name, times in schedule.items():
        print(f"\n📅 {day_name.upper()}:")
        
        for time_str in times:
            # Парсим время
            hour, minute = map(int, time_str.split(':'))
            
            # Вычисляем дату публикации
            today = datetime.now()
            days_ahead = list(schedule.keys()).index(day_name)
            if days_ahead == 0:  # Сегодня
                publish_date = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if publish_date < today:
                    publish_date += timedelta(days=7)  # На следующую неделю
            else:
                publish_date = today + timedelta(days=days_ahead)
                publish_date = publish_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            print(f"   ⏰ {time_str} - {publish_date.strftime('%Y-%m-%d %H:%M')}")
            
            # Создаем посты для каждого канала
            for channel in channels:
                try:
                    # Генерируем контент
                    audience = audiences[total_posts % len(audiences)]
                    content_type = content_types[total_posts % len(content_types)]
                    
                    content = generator.generate_content(audience, content_type)
                    
                    # Создаем пост
                    post_data = {
                        "content": content,
                        "channel_id": channel['chat_id'],
                        "scheduled_time": publish_date.isoformat(),
                        "media_path": None,
                        "media_type": None
                    }
                    
                    response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"      ✅ {channel['name']}: {audience} - {content_type}")
                        total_posts += 1
                    else:
                        print(f"      ❌ {channel['name']}: ошибка {response.status_code}")
                        
                except Exception as e:
                    print(f"      ❌ {channel['name']}: {e}")
                
                time.sleep(0.5)  # Пауза между запросами
    
    print(f"\n🎯 ИТОГО ЗАПЛАНИРОВАНО: {total_posts} постов")
    return total_posts

def setup_daily_content():
    """Настраивает ежедневный контент"""
    print("\n📝 НАСТРОЙКА ЕЖЕДНЕВНОГО КОНТЕНТА")
    print("="*50)
    
    # Ежедневные темы
    daily_themes = {
        'monday': {
            'theme': 'Мотивация на неделю',
            'audience': 'Новички в дизайне',
            'content_type': 'Мотивация'
        },
        'tuesday': {
            'theme': 'Практический совет',
            'audience': 'Junior дизайнеры',
            'content_type': 'Совет'
        },
        'wednesday': {
            'theme': 'Разбор кейса',
            'audience': 'Фрилансеры',
            'content_type': 'Кейс'
        },
        'thursday': {
            'theme': 'Решение проблемы',
            'audience': 'Разработчики',
            'content_type': 'Решение'
        },
        'friday': {
            'theme': 'Преимущества обучения',
            'audience': 'Новички в дизайне',
            'content_type': 'Преимущества курса'
        },
        'saturday': {
            'theme': 'Выходной совет',
            'audience': 'Junior дизайнеры',
            'content_type': 'Совет'
        },
        'sunday': {
            'theme': 'Подготовка к неделе',
            'audience': 'Фрилансеры',
            'content_type': 'Мотивация'
        }
    }
    
    channels = [
        {'chat_id': '-1002091962525', 'name': 'digoGraphickDesign'},
        {'chat_id': '-1002123538949', 'name': 'digoUI'}
    ]
    
    generator = ContentGenerator()
    
    for day, theme_info in daily_themes.items():
        print(f"\n📅 {day.upper()}: {theme_info['theme']}")
        
        # Время публикации: 10:00 каждый день
        publish_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        days_ahead = list(daily_themes.keys()).index(day)
        publish_time += timedelta(days=days_ahead)
        
        for channel in channels:
            try:
                content = generator.generate_content(
                    theme_info['audience'], 
                    theme_info['content_type']
                )
                
                post_data = {
                    "content": content,
                    "channel_id": channel['chat_id'],
                    "scheduled_time": publish_time.isoformat(),
                    "media_path": None,
                    "media_type": None
                }
                
                response = requests.post("http://localhost:8000/api/posts", json=post_data, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ {channel['name']}: {theme_info['audience']} - {theme_info['content_type']}")
                else:
                    print(f"   ❌ {channel['name']}: ошибка")
                    
            except Exception as e:
                print(f"   ❌ {channel['name']}: {e}")
            
            time.sleep(0.5)

def check_schedule_status():
    """Проверяет статус расписания"""
    print("\n📊 ПРОВЕРКА СТАТУСА РАСПИСАНИЯ")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:8000/api/posts", timeout=5)
        if response.status_code == 200:
            posts = response.json()
            
            scheduled_posts = [post for post in posts if not post.get('published', False)]
            published_posts = [post for post in posts if post.get('published', False)]
            
            print(f"📈 Статистика:")
            print(f"   • Всего постов: {len(posts)}")
            print(f"   • Опубликовано: {len(published_posts)}")
            print(f"   • Запланировано: {len(scheduled_posts)}")
            
            if scheduled_posts:
                print(f"\n⏳ Ближайшие публикации:")
                # Сортируем по времени
                scheduled_posts.sort(key=lambda x: x.get('scheduled_time', ''))
                
                for i, post in enumerate(scheduled_posts[:10], 1):  # Показываем первые 10
                    scheduled_time = post.get('scheduled_time', 'N/A')
                    channel_name = post.get('channel_name', 'N/A')
                    content_preview = post.get('content', '')[:50] + "..."
                    
                    print(f"   {i}. {scheduled_time} | {channel_name}")
                    print(f"      📄 {content_preview}")
                    print()
                    
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    print("🚀 НАСТРОЙКА АВТОМАТИЧЕСКОГО РАСПИСАНИЯ")
    print("="*60)
    
    try:
        # Настраиваем основное расписание
        total_posts = setup_auto_schedule()
        
        # Настраиваем ежедневный контент
        setup_daily_content()
        
        # Проверяем результат
        check_schedule_status()
        
        print("\n" + "="*60)
        print("✅ АВТОМАТИЧЕСКОЕ РАСПИСАНИЕ НАСТРОЕНО!")
        print("="*60)
        print(f"📊 Всего запланировано: {total_posts + 14} постов")
        print("📅 Планировщик будет автоматически публиковать посты")
        print("🔍 Мониторинг: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 