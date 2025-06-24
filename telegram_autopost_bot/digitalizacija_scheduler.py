#!/usr/bin/env python3
"""
Система автоматического постинга для кампании "Digitalizacija Biznesa"
"""

import telebot
import os
import json
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random
import sqlite3

load_dotenv()

class DigitalizacijaScheduler:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot = telebot.TeleBot(self.bot_token)
        
        # Загружаем конфигурацию каналов
        from config import DIGITALIZACIJA_CHANNELS, POSTING_SCHEDULE, POST_TEMPLATES
        
        self.channels = DIGITALIZACIJA_CHANNELS
        self.schedule = POSTING_SCHEDULE['digitalizacija']
        self.templates = POST_TEMPLATES['digitalizacija']
        
        # База данных для постов
        self.db_path = 'data/digitalizacija_posts.db'
        self.init_database()
        
        # Контент для постов
        self.content_library = self.load_content_library()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица для постов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                post_type TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                scheduled_time DATETIME,
                sent_time DATETIME,
                status TEXT DEFAULT 'pending',
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для расписания
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posting_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                post_type TEXT,
                active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_content_library(self):
        """Загрузка библиотеки контента"""
        return {
            'educational': [
                {
                    'title': 'Что такое цифровизация бизнеса?',
                    'content': 'Цифровизация бизнеса — это внедрение цифровых технологий для автоматизации и оптимизации бизнес-процессов.',
                    'tip': 'Начните с аудита текущих процессов',
                    'statistic': '78% компаний планируют увеличить инвестиции в цифровизацию',
                    'question': 'Какие процессы в вашем бизнесе можно автоматизировать?'
                },
                {
                    'title': 'CRM-системы для малого бизнеса',
                    'content': 'CRM помогает управлять клиентами, отслеживать сделки и автоматизировать продажи.',
                    'tip': 'Выбирайте CRM с учетом размера команды',
                    'statistic': 'CRM увеличивает продажи на 29%',
                    'question': 'Используете ли вы CRM в своем бизнесе?'
                },
                {
                    'title': 'Email-маркетинг: основы',
                    'content': 'Email-маркетинг остается одним из самых эффективных каналов привлечения клиентов.',
                    'tip': 'Персонализируйте письма для повышения открытий',
                    'statistic': 'ROI email-маркетинга составляет 3800%',
                    'question': 'Какой у вас процент открытий email-писем?'
                }
            ],
            'problem': [
                {
                    'title': '5 признаков того, что ваш бизнес отстает',
                    'problem_description': 'Медленные процессы, потеря клиентов, отсутствие аналитики — все это сигналы для цифровизации.',
                    'consequences': 'Потеря конкурентных преимуществ, снижение прибыли, усталость команды.',
                    'diagnosis': 'Проведите аудит процессов и определите узкие места.',
                    'solution': 'Внедрите CRM, автоматизируйте маркетинг, настройте аналитику.',
                    'call_to_action': 'Получите бесплатный аудит вашего бизнеса'
                },
                {
                    'title': 'Почему клиенты уходят к конкурентам?',
                    'problem_description': 'Медленная обработка заявок, отсутствие персонализации, плохой клиентский сервис.',
                    'consequences': 'Потеря клиентов, снижение лояльности, негативные отзывы.',
                    'diagnosis': 'Проанализируйте воронку продаж и точки контакта с клиентами.',
                    'solution': 'Автоматизируйте обработку заявок, внедрите чат-боты, улучшите сервис.',
                    'call_to_action': 'Узнайте, как удержать клиентов'
                }
            ],
            'selling': [
                {
                    'title': 'Научитесь цифровизировать бизнес за 30 дней',
                    'problem': 'Не знаете, с чего начать цифровизацию?',
                    'advantages': 'Пошаговые инструкции, практические кейсы, поддержка экспертов',
                    'results': 'Автоматизация процессов, рост продаж, экономия времени',
                    'bonuses': 'Бесплатные материалы, консультации, доступ к сообществу',
                    'limitation': 'Только 50 мест по специальной цене',
                    'call_to_action': 'Записаться на курс'
                }
            ],
            'case_study': [
                {
                    'title': 'Как кафе увеличило выручку на 40%',
                    'company_description': 'Небольшое кафе в центре города',
                    'problem': 'Хаос в заказах, потеря клиентов, неэффективное управление',
                    'solution': 'Внедрение CRM, автоматизация заказов, аналитика продаж',
                    'results': 'Рост выручки на 40%, сокращение времени обработки заказов в 3 раза',
                    'conclusions': 'Цифровизация доступна даже малому бизнесу'
                }
            ]
        }
    
    def generate_post_content(self, post_type, channel_id):
        """Генерация контента поста"""
        if post_type in self.content_library:
            content = random.choice(self.content_library[post_type])
            
            # Применяем шаблон
            template = self.templates.get(post_type, '')
            
            if template:
                return template.format(**content)
            else:
                return f"{content.get('title', '')}\n\n{content.get('content', '')}"
        
        return None
    
    def schedule_post(self, channel_id, post_type, scheduled_time):
        """Планирование поста"""
        content = self.generate_post_content(post_type, channel_id)
        
        if content:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO posts (title, content, post_type, channel_id, scheduled_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                content[:100] + '...' if len(content) > 100 else content,
                content,
                post_type,
                channel_id,
                scheduled_time,
                'pending'
            ))
            
            post_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Пост запланирован: {post_type} в {channel_id} на {scheduled_time}")
            return post_id
        
        return None
    
    def send_post(self, post_id):
        """Отправка поста"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        post = cursor.fetchone()
        
        if post:
            try:
                # Отправляем пост
                result = self.bot.send_message(
                    chat_id=post[4],  # channel_id
                    text=post[2],     # content
                    parse_mode='Markdown'
                )
                
                if result:
                    # Обновляем статус
                    cursor.execute('''
                        UPDATE posts 
                        SET status = ?, sent_time = ?
                        WHERE id = ?
                    ''', ('sent', datetime.now(), post_id))
                    
                    conn.commit()
                    print(f"✅ Пост {post_id} отправлен в {post[4]}")
                    return True
                else:
                    print(f"❌ Ошибка при отправке поста {post_id}")
                    return False
                    
            except Exception as e:
                print(f"❌ Ошибка при отправке поста {post_id}: {e}")
                return False
        
        conn.close()
        return False
    
    def get_pending_posts(self):
        """Получение запланированных постов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM posts 
            WHERE status = 'pending' 
            AND scheduled_time <= ?
            ORDER BY scheduled_time
        ''', (datetime.now(),))
        
        posts = cursor.fetchall()
        conn.close()
        
        return posts
    
    def schedule_weekly_content(self):
        """Планирование контента на неделю"""
        print("📅 Планирование контента на неделю...")
        
        # Определяем время публикации для каждого дня
        for day, times in self.schedule.items():
            for time_slot in times:
                # Выбираем случайный канал
                channel_key = random.choice(list(self.channels.keys()))
                channel_id = self.channels[channel_key]['chat_id']
                
                # Выбираем тип поста
                post_types = ['educational', 'problem', 'selling', 'case_study']
                post_type = random.choice(post_types)
                
                # Планируем время
                scheduled_time = self.parse_schedule_time(day, time_slot)
                
                # Создаем пост
                self.schedule_post(channel_id, post_type, scheduled_time)
    
    def parse_schedule_time(self, day, time_slot):
        """Парсинг времени расписания"""
        # Определяем день недели
        days_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        day_num = days_map.get(day.lower(), 0)
        
        # Парсим время
        hour, minute = map(int, time_slot.split(':'))
        
        # Находим следующий день недели
        today = datetime.now()
        days_ahead = day_num - today.weekday()
        
        if days_ahead <= 0:  # Прошло в этом году
            days_ahead += 7
        
        target_date = today + timedelta(days=days_ahead)
        scheduled_time = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return scheduled_time
    
    def run_scheduler(self):
        """Запуск планировщика"""
        print("🚀 Запуск планировщика постов...")
        
        # Планируем задачи
        schedule.every().hour.do(self.check_pending_posts)
        schedule.every().monday.at("09:00").do(self.schedule_weekly_content)
        
        print("✅ Планировщик запущен")
        print("📅 Проверка постов каждый час")
        print("📅 Планирование контента каждый понедельник в 9:00")
        
        # Запускаем планировщик
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
    
    def check_pending_posts(self):
        """Проверка запланированных постов"""
        pending_posts = self.get_pending_posts()
        
        for post in pending_posts:
            self.send_post(post[0])  # post_id
    
    def get_statistics(self):
        """Получение статистики постов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Общая статистика
        cursor.execute('SELECT COUNT(*) FROM posts')
        total_posts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM posts WHERE status = "sent"')
        sent_posts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM posts WHERE status = "pending"')
        pending_posts = cursor.fetchone()[0]
        
        # Статистика по каналам
        cursor.execute('''
            SELECT channel_id, COUNT(*) 
            FROM posts 
            WHERE status = "sent" 
            GROUP BY channel_id
        ''')
        channel_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_posts': total_posts,
            'sent_posts': sent_posts,
            'pending_posts': pending_posts,
            'channel_stats': channel_stats
        }
    
    def create_test_posts(self):
        """Создание тестовых постов"""
        print("🧪 Создание тестовых постов...")
        
        # Создаем посты для каждого канала
        for channel_key, channel_info in self.channels.items():
            channel_id = channel_info['chat_id']
            
            # Создаем посты разных типов
            for post_type in ['educational', 'problem', 'selling', 'case_study']:
                scheduled_time = datetime.now() + timedelta(minutes=random.randint(1, 10))
                self.schedule_post(channel_id, post_type, scheduled_time)
        
        print("✅ Тестовые посты созданы")

def main():
    """Основная функция"""
    scheduler = DigitalizacijaScheduler()
    
    # Создаем тестовые посты
    scheduler.create_test_posts()
    
    # Планируем контент на неделю
    scheduler.schedule_weekly_content()
    
    # Запускаем планировщик
    scheduler.run_scheduler()

if __name__ == "__main__":
    main() 