#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API и базы данных
"""

import sqlite3
import os
from datetime import datetime, timedelta
from database import Database
from integrated_content_generator import ContentGenerator

def test_database():
    """Тестирует базу данных"""
    print("🗄️ Тестирование базы данных...")
    
    # Создаем тестовую базу данных
    db_path = 'data/test_posts.db'
    
    # Удаляем старую тестовую БД если есть
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Создаем директорию если нет
    os.makedirs('data', exist_ok=True)
    
    try:
        # Создаем соединение с БД
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                chat_id TEXT NOT NULL UNIQUE,
                active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                published BOOLEAN DEFAULT FALSE,
                published_time DATETIME,
                error_message TEXT,
                media_path TEXT,
                media_type TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Добавляем тестовые данные
        cursor.execute('''
            INSERT INTO channels (name, chat_id, active) VALUES 
            ('Test Channel', '-1001234567890', TRUE),
            ('Main Channel', '-1009876543210', TRUE)
        ''')
        
        # Добавляем тестовые посты
        test_time = datetime.now() + timedelta(hours=1)
        cursor.execute('''
            INSERT INTO posts (content, channel_id, scheduled_time) VALUES 
            ('Тестовый пост 1', '-1001234567890', ?),
            ('Тестовый пост 2', '-1009876543210', ?)
        ''', (test_time, test_time + timedelta(hours=2)))
        
        conn.commit()
        
        # Проверяем данные
        cursor.execute('SELECT COUNT(*) FROM channels')
        channels_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM posts')
        posts_count = cursor.fetchone()[0]
        
        print(f"✅ База данных создана успешно!")
        print(f"   • Каналов: {channels_count}")
        print(f"   • Постов: {posts_count}")
        
        # Показываем каналы
        cursor.execute('SELECT * FROM channels')
        channels = cursor.fetchall()
        print(f"\n📢 Каналы в базе:")
        for channel in channels:
            print(f"   • {channel[1]} (ID: {channel[2]}) - {'Активен' if channel[3] else 'Неактивен'}")
        
        # Показываем посты
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
        print(f"\n📝 Посты в базе:")
        for post in posts:
            print(f"   • ID: {post[0]} | Контент: {post[1][:50]}... | Время: {post[3]}")
        
        conn.close()
        
        # Удаляем тестовую БД
        os.remove(db_path)
        print(f"\n🧹 Тестовая база данных удалена")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании базы данных: {e}")
        return False

def test_database_class():
    """Тестирует класс Database"""
    print("\n🔧 Тестирование класса Database...")
    
    try:
        # Создаем экземпляр Database
        db = Database('data/test_db.db')
        
        # Тестируем добавление канала
        db.add_channel('Test Channel', '-1001234567890')
        print("✅ Канал добавлен")
        
        # Тестируем получение каналов
        channels = db.get_active_channels()
        print(f"✅ Получено каналов: {len(channels)}")
        
        # Тестируем добавление поста
        test_time = datetime.now() + timedelta(hours=1)
        post_id = db.add_post(
            content='Тестовый пост через Database класс',
            channel_id='-1001234567890',
            scheduled_time=test_time
        )
        print(f"✅ Пост добавлен с ID: {post_id}")
        
        # Тестируем получение постов
        posts = db.get_pending_posts()
        print(f"✅ Получено постов: {len(posts)}")
        
        # Очищаем тестовую БД
        if os.path.exists('data/test_db.db'):
            os.remove('data/test_db.db')
        
        print("✅ Класс Database работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании класса Database: {e}")
        return False

def test_content_integration():
    """Тестирует интеграцию генератора контента с базой данных"""
    print("\n🔄 Тестирование интеграции генератора контента...")
    
    try:
        # Создаем генератор и базу данных
        generator = ContentGenerator()
        db = Database('data/test_integration.db')
        
        # Добавляем тестовый канал
        db.add_channel('Integration Test Channel', '-1001234567890')
        
        # Генерируем контент
        content = generator.generate_content('Новички в дизайне', 'Совет')
        
        # Добавляем в базу данных
        test_time = datetime.now() + timedelta(hours=1)
        post_id = db.add_post(
            content=content,
            channel_id='-1001234567890',
            scheduled_time=test_time
        )
        
        print(f"✅ Контент сгенерирован и добавлен в БД с ID: {post_id}")
        print(f"📝 Содержание: {content[:100]}...")
        
        # Проверяем что пост в базе
        posts = db.get_pending_posts()
        print(f"✅ Постов в базе: {len(posts)}")
        
        # Очищаем тестовую БД
        if os.path.exists('data/test_integration.db'):
            os.remove('data/test_integration.db')
        
        print("✅ Интеграция работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании интеграции: {e}")
        return False

def test_scheduler():
    """Тестирует планировщик"""
    print("\n⏰ Тестирование планировщика...")
    
    try:
        from scheduler import PostScheduler
        from aiogram import Bot
        
        # Создаем мок-бот для тестирования
        class MockBot:
            async def send_message(self, chat_id, text):
                print(f"🤖 Мок-бот отправил сообщение в {chat_id}: {text[:50]}...")
                return True
        
        # Создаем базу данных и планировщик
        db = Database('data/test_scheduler.db')
        db.add_channel('Scheduler Test Channel', '-1001234567890')
        
        # Добавляем тестовый пост
        test_time = datetime.now() + timedelta(seconds=5)  # Через 5 секунд
        db.add_post(
            content='Тестовый пост для планировщика',
            channel_id='-1001234567890',
            scheduled_time=test_time
        )
        
        # Создаем планировщик
        scheduler = PostScheduler(db, MockBot(), {})
        
        print("✅ Планировщик создан")
        print("⏳ Ожидание 10 секунд для тестирования...")
        
        # Запускаем планировщик на короткое время
        import asyncio
        async def test_scheduler_run():
            await scheduler.start()
            await asyncio.sleep(10)
            await scheduler.stop()
        
        asyncio.run(test_scheduler_run())
        
        # Очищаем тестовую БД
        if os.path.exists('data/test_scheduler.db'):
            os.remove('data/test_scheduler.db')
        
        print("✅ Планировщик работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании планировщика: {e}")
        return False

if __name__ == "__main__":
    print("🔧 ЗАПУСК ТЕСТИРОВАНИЯ API И БАЗЫ ДАННЫХ")
    print("="*60)
    
    results = []
    
    try:
        results.append(test_database())
        results.append(test_database_class())
        results.append(test_content_integration())
        results.append(test_scheduler())
        
        print("\n" + "="*60)
        success_count = sum(results)
        total_count = len(results)
        
        if success_count == total_count:
            print(f"✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ({success_count}/{total_count})")
        else:
            print(f"⚠️ ПРОЙДЕНО ТЕСТОВ: {success_count}/{total_count}")
        
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 