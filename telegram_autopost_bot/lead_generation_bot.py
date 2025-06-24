#!/usr/bin/env python3
"""
Система лидогенерации для кампании "Digitalizacija Biznesa"
"""

import telebot
from telebot import types
import sqlite3
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import schedule
import time
import threading

load_dotenv()

class LeadGenerationBot:
    def __init__(self):
        self.bot_token = os.getenv('LEAD_BOT_TOKEN') or os.getenv('BOT_TOKEN')
        self.admin_id = int(os.getenv('ADMIN_ID', 0))
        self.bot = telebot.TeleBot(self.bot_token)
        
        # База данных для лидов
        self.db_path = 'data/digitalizacija_leads.db'
        self.init_database()
        
        # Воронка продаж
        self.sales_funnel = {
            'awareness': 'Осведомленность',
            'interest': 'Интерес', 
            'consideration': 'Рассмотрение',
            'intent': 'Намерение',
            'purchase': 'Покупка'
        }
        
        # Настройка обработчиков
        self.setup_handlers()
        
        # Бесплатные материалы
        self.free_materials = {
            'guide': {
                'title': '10 шагов к цифровизации бизнеса',
                'file': 'content-folder/digitalizacija/materials/guides/10_steps_digitalization.md',
                'description': 'Пошаговый план внедрения цифровых технологий в ваш бизнес'
            },
            'crm_guide': {
                'title': 'Выбор CRM-системы для малого бизнеса',
                'file': 'content-folder/digitalizacija/materials/guides/crm_selection_guide.md',
                'description': 'Сравнение лучших CRM-систем и рекомендации по выбору'
            },
            'automation_templates': {
                'title': 'Шаблоны для автоматизации процессов',
                'file': 'content-folder/digitalizacija/materials/guides/automation_templates.md',
                'description': 'Готовые шаблоны для автоматизации основных бизнес-процессов'
            }
        }
    
    def init_database(self):
        """Инициализация базы данных для лидов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица лидов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                business_type TEXT,
                business_size TEXT,
                current_stage TEXT DEFAULT 'awareness',
                source TEXT DEFAULT 'bot',
                interests TEXT,
                pain_points TEXT,
                budget TEXT,
                timeline TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица взаимодействий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES leads (user_id)
            )
        ''')
        
        # Таблица конверсий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                from_stage TEXT,
                to_stage TEXT,
                trigger TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES leads (user_id)
            )
        ''')
        
        # Таблица материалов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials_sent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                material_type TEXT,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES leads (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.handle_start(message)
        
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.handle_help(message)
        
        @self.bot.message_handler(commands=['status'])
        def status_command(message):
            self.handle_status(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            self.handle_message(message)
    
    def handle_start(self, message):
        """Обработка команды /start"""
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        
        # Создаем или обновляем лида
        self.create_or_update_lead(user_id, username, first_name, last_name)
        
        # Создаем главное меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🎯 Получить бесплатный гайд")
        btn2 = types.KeyboardButton("📞 Консультация")
        btn3 = types.KeyboardButton("💳 Записаться на курс")
        btn4 = types.KeyboardButton("📊 Аудит бизнеса")
        btn5 = types.KeyboardButton("❓ Частые вопросы")
        btn6 = types.KeyboardButton("👥 Наше сообщество")
        
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
        welcome_text = f"""
🚀 Добро пожаловать в мир цифровизации бизнеса, {first_name}!

Я помогу вам:

✅ **Автоматизировать процессы**
• CRM-системы для управления клиентами
• Автоматизация маркетинга и продаж
• Чат-боты и интеграции

✅ **Внедрить цифровой маркетинг**
• Email-маркетинг
• Социальные сети
• Контекстная реклама

✅ **Настроить аналитику**
• KPI и метрики
• Дашборды и отчеты
• Принятие решений на основе данных

✅ **Масштабировать бизнес**
• Облачные решения
• Инструменты роста
• Стратегии развития

🎁 **Бесплатные материалы:**
• Чек-лист "10 шагов к цифровизации"
• Гайд "Выбор CRM-системы"
• Шаблоны для автоматизации

Выберите, что вас интересует:
        """
        
        self.bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'start', 'Пользователь запустил бота')
    
    def handle_help(self, message):
        """Обработка команды /help"""
        help_text = """
🤖 **Помощь по использованию бота**

**Основные команды:**
/start - Запуск бота и главное меню
/help - Показать эту справку
/status - Проверить статус вашей заявки

**Что вы можете получить:**
🎯 Бесплатные материалы по цифровизации
📞 Персональную консультацию
💳 Запись на курс "Digitalizacija Biznesa"
📊 Аудит вашего бизнеса

**Наши каналы:**
📺 @digitalizacija_biznesa - Основной канал
⚙️ @biznes_automation - Кейсы автоматизации
🚀 @startup_digital - Для стартапов

**Наши группы:**
👥 @digitalizacija_community - Сообщество
💼 @biznes_consulting - Консультации
💡 @automation_tips - Советы

**Поддержка:**
Если у вас есть вопросы, пишите в группу @digitalizacija_community
        """
        
        self.bot.send_message(
            message.chat.id,
            help_text,
            parse_mode='Markdown'
        )
    
    def handle_status(self, message):
        """Обработка команды /status"""
        user_id = message.from_user.id
        
        # Получаем информацию о лиде
        lead_info = self.get_lead_info(user_id)
        
        if lead_info:
            status_text = f"""
📊 **Статус вашей заявки**

👤 **Ваши данные:**
Имя: {lead_info['first_name']} {lead_info['last_name']}
Бизнес: {lead_info['business_type'] or 'Не указан'}
Размер: {lead_info['business_size'] or 'Не указан'}

🎯 **Текущий этап:** {self.sales_funnel.get(lead_info['current_stage'], 'Неизвестно')}

📅 **Дата регистрации:** {lead_info['created_at']}

📋 **Полученные материалы:**
{self.get_materials_sent(user_id)}

**Следующие шаги:**
{self.get_next_steps(lead_info['current_stage'])}
            """
        else:
            status_text = "❌ Информация не найдена. Попробуйте /start"
        
        self.bot.send_message(
            message.chat.id,
            status_text,
            parse_mode='Markdown'
        )
    
    def handle_message(self, message):
        """Обработка всех сообщений"""
        user_id = message.from_user.id
        text = message.text
        
        if text == "🎯 Получить бесплатный гайд":
            self.handle_free_guide(message)
        elif text == "📞 Консультация":
            self.handle_consultation(message)
        elif text == "💳 Записаться на курс":
            self.handle_course_registration(message)
        elif text == "📊 Аудит бизнеса":
            self.handle_business_audit(message)
        elif text == "❓ Частые вопросы":
            self.handle_faq(message)
        elif text == "👥 Наше сообщество":
            self.handle_community(message)
        else:
            # Обрабатываем как обычное сообщение
            self.handle_general_message(message)
    
    def handle_free_guide(self, message):
        """Обработка запроса бесплатного гайда"""
        user_id = message.from_user.id
        
        # Создаем inline клавиатуру для выбора материала
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for key, material in self.free_materials.items():
            btn = types.InlineKeyboardButton(
                f"📄 {material['title']}",
                callback_data=f"material_{key}"
            )
            markup.add(btn)
        
        text = """
🎁 **Выберите бесплатный материал:**

📄 **10 шагов к цифровизации бизнеса**
Пошаговый план внедрения цифровых технологий

📄 **Выбор CRM-системы для малого бизнеса**
Сравнение лучших CRM-систем и рекомендации

📄 **Шаблоны для автоматизации процессов**
Готовые шаблоны для автоматизации

Выберите материал, который хотите получить:
        """
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'free_guide_request', 'Запрос бесплатного гайда')
        
        # Переводим в стадию "Интерес"
        self.move_lead_stage(user_id, 'awareness', 'interest', 'Запрос бесплатного материала')
    
    def handle_consultation(self, message):
        """Обработка запроса консультации"""
        user_id = message.from_user.id
        
        # Запрашиваем контактную информацию
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton("📱 Отправить номер телефона", request_contact=True)
        markup.add(btn)
        
        text = """
📞 **Запись на консультацию**

Для записи на персональную консультацию нам нужна ваша контактная информация.

**Что включает консультация:**
✅ Аудит текущих процессов
✅ Рекомендации по автоматизации
✅ План цифровизации
✅ Подбор инструментов
✅ Расчет ROI

**Длительность:** 30-45 минут
**Стоимость:** Бесплатно

Нажмите кнопку ниже, чтобы отправить номер телефона:
        """
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'consultation_request', 'Запрос консультации')
        
        # Переводим в стадию "Рассмотрение"
        self.move_lead_stage(user_id, 'interest', 'consideration', 'Запрос консультации')
    
    def handle_course_registration(self, message):
        """Обработка записи на курс"""
        user_id = message.from_user.id
        
        # Создаем inline клавиатуру для выбора тарифа
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        btn1 = types.InlineKeyboardButton(
            "💎 Премиум (полный курс + поддержка)",
            callback_data="course_premium"
        )
        btn2 = types.InlineKeyboardButton(
            "📚 Стандарт (основной курс)",
            callback_data="course_standard"
        )
        btn3 = types.InlineKeyboardButton(
            "🎯 Базовый (основы цифровизации)",
            callback_data="course_basic"
        )
        
        markup.add(btn1, btn2, btn3)
        
        text = """
💳 **Запись на курс "Digitalizacija Biznesa"**

**Выберите подходящий тариф:**

💎 **Премиум** - $297
• Полный курс (5 модулей)
• Персональная поддержка
• Доступ к сообществу
• Бонусные материалы
• Сертификат

📚 **Стандарт** - $197
• Основной курс (5 модулей)
• Групповая поддержка
• Доступ к сообществу
• Сертификат

🎯 **Базовый** - $97
• Основы цифровизации (2 модуля)
• Базовые материалы
• Сертификат

**Выберите тариф:**
        """
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'course_registration', 'Запрос записи на курс')
        
        # Переводим в стадию "Намерение"
        self.move_lead_stage(user_id, 'consideration', 'intent', 'Запрос записи на курс')
    
    def handle_business_audit(self, message):
        """Обработка запроса аудита бизнеса"""
        user_id = message.from_user.id
        
        # Создаем форму для сбора информации
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        btn1 = types.KeyboardButton("🏢 Малый бизнес (1-10 сотрудников)")
        btn2 = types.KeyboardButton("🏭 Средний бизнес (11-50 сотрудников)")
        btn3 = types.KeyboardButton("🏢 Крупный бизнес (50+ сотрудников)")
        btn4 = types.KeyboardButton("👤 ИП/Фрилансер")
        
        markup.add(btn1, btn2, btn3, btn4)
        
        text = """
📊 **Аудит бизнеса**

Для проведения аудита нам нужно узнать больше о вашем бизнесе.

**Что включает аудит:**
✅ Анализ текущих процессов
✅ Оценка уровня цифровизации
✅ Выявление узких мест
✅ Рекомендации по улучшению
✅ План внедрения

**Выберите размер вашего бизнеса:**
        """
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'audit_request', 'Запрос аудита бизнеса')
    
    def handle_faq(self, message):
        """Обработка частых вопросов"""
        faq_text = """
❓ **Частые вопросы**

**Q: Сколько времени нужно для цифровизации?**
A: От 1 до 6 месяцев в зависимости от сложности и размера бизнеса.

**Q: Какие инструменты нужны?**
A: CRM-система, инструменты автоматизации, аналитика. Конкретный список зависит от ваших задач.

**Q: Сколько это стоит?**
A: От $50 до $500 в месяц на инструменты. ROI обычно составляет 300-500%.

**Q: Нужны ли технические знания?**
A: Базовые навыки работы с компьютером. Мы обучаем всему с нуля.

**Q: Можно ли начать с малого?**
A: Да! Рекомендуем начинать с автоматизации 1-2 процессов.

**Q: Какой результат я получу?**
A: Экономия времени 30-50%, рост продаж 20-40%, улучшение клиентского сервиса.

**Есть другие вопросы? Пишите в группу @digitalizacija_community**
        """
        
        self.bot.send_message(
            message.chat.id,
            faq_text,
            parse_mode='Markdown'
        )
    
    def handle_community(self, message):
        """Обработка информации о сообществе"""
        community_text = """
👥 **Наше сообщество**

**Основная группа:** @digitalizacija_community
• Обсуждение тем курса
• Вопросы и ответы
• Обмен опытом
• Нетворкинг

**Консультации:** @biznes_consulting
• Персональные консультации
• Аудит процессов
• Техническая поддержка

**Советы:** @automation_tips
• Лайфхаки автоматизации
• Обзоры инструментов
• Пошаговые инструкции

**Каналы:**
📺 @digitalizacija_biznesa - Основной канал
⚙️ @biznes_automation - Кейсы автоматизации
🚀 @startup_digital - Для стартапов

**Присоединяйтесь к сообществу!**
        """
        
        self.bot.send_message(
            message.chat.id,
            community_text,
            parse_mode='Markdown'
        )
    
    def handle_general_message(self, message):
        """Обработка общих сообщений"""
        user_id = message.from_user.id
        text = message.text
        
        # Простая обработка текста
        if any(word in text.lower() for word in ['привет', 'здравствуйте', 'добрый день']):
            response = f"Привет! 👋 Чем могу помочь?"
        elif any(word in text.lower() for word in ['спасибо', 'благодарю']):
            response = "Пожалуйста! 😊 Если есть вопросы, обращайтесь."
        elif any(word in text.lower() for word in ['цена', 'стоимость', 'сколько стоит']):
            response = "Стоимость курса от $97 до $297. Подробности: 💳 Записаться на курс"
        elif any(word in text.lower() for word in ['время', 'длительность', 'сколько времени']):
            response = "Курс рассчитан на 30 дней. Можно проходить в своем темпе."
        else:
            response = """
Не совсем понял ваш вопрос. 🤔

Попробуйте выбрать один из вариантов в меню или напишите в группу @digitalizacija_community

Также можете использовать команду /help для получения справки.
            """
        
        self.bot.send_message(message.chat.id, response)
        
        # Записываем взаимодействие
        self.record_interaction(user_id, 'general_message', f'Сообщение: {text[:100]}')
    
    def create_or_update_lead(self, user_id, username, first_name, last_name):
        """Создание или обновление лида"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO leads 
            (user_id, username, first_name, last_name, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_lead_info(self, user_id):
        """Получение информации о лиде"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM leads WHERE user_id = ?', (user_id,))
        lead = cursor.fetchone()
        
        conn.close()
        
        if lead:
            return {
                'user_id': lead[1],
                'username': lead[2],
                'first_name': lead[3],
                'last_name': lead[4],
                'phone': lead[5],
                'email': lead[6],
                'business_type': lead[7],
                'business_size': lead[8],
                'current_stage': lead[9],
                'created_at': lead[15]
            }
        
        return None
    
    def record_interaction(self, user_id, action, data):
        """Запись взаимодействия"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions (user_id, action, data)
            VALUES (?, ?, ?)
        ''', (user_id, action, data))
        
        conn.commit()
        conn.close()
    
    def move_lead_stage(self, user_id, from_stage, to_stage, trigger):
        """Перемещение лида по воронке"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Обновляем стадию лида
        cursor.execute('''
            UPDATE leads 
            SET current_stage = ?, updated_at = ?
            WHERE user_id = ?
        ''', (to_stage, datetime.now(), user_id))
        
        # Записываем конверсию
        cursor.execute('''
            INSERT INTO conversions (user_id, from_stage, to_stage, trigger)
            VALUES (?, ?, ?, ?)
        ''', (user_id, from_stage, to_stage, trigger))
        
        conn.commit()
        conn.close()
    
    def get_materials_sent(self, user_id):
        """Получение списка отправленных материалов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT material_type FROM materials_sent 
            WHERE user_id = ?
            ORDER BY sent_at
        ''', (user_id,))
        
        materials = cursor.fetchall()
        conn.close()
        
        if materials:
            return '\n'.join([f"• {material[0]}" for material in materials])
        else:
            return "Пока не получены"
    
    def get_next_steps(self, current_stage):
        """Получение следующих шагов для стадии"""
        steps = {
            'awareness': "Получите бесплатный гайд для знакомства с темой",
            'interest': "Запишитесь на консультацию для детального разбора",
            'consideration': "Пройдите аудит бизнеса для оценки возможностей",
            'intent': "Выберите подходящий тариф курса",
            'purchase': "Начните обучение и внедрение"
        }
        
        return steps.get(current_stage, "Продолжайте изучение материалов")
    
    def run(self):
        """Запуск бота"""
        print("🤖 Запуск бота лидогенерации...")
        self.bot.polling(none_stop=True)

def main():
    """Основная функция"""
    bot = LeadGenerationBot()
    bot.run()

if __name__ == "__main__":
    main() 