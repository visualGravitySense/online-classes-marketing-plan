#!/usr/bin/env python3
"""
Система приветственных постов для кампании "Digitalizacija Biznesa"
"""

import telebot
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

class WelcomePostsManager:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot = telebot.TeleBot(self.bot_token)
        
        # Приветственные посты для каждого канала
        self.welcome_posts = {
            'digitalizacija_main': {
                'title': '🚀 Добро пожаловать в Digitalizacija Biznesa!',
                'content': """🎯 Основной канал курса по цифровизации бизнеса

Здесь вы найдете:

📊 Автоматизация процессов
• CRM-системы для малого бизнеса
• Автоматизация маркетинга
• Чат-боты и интеграции

💻 Цифровой маркетинг
• Email-маркетинг
• Социальные сети
• Контекстная реклама

📈 Аналитика и метрики
• KPI для бизнеса
• Дашборды и отчеты
• Принятие решений на основе данных

🚀 Масштабирование
• Облачные решения
• Инструменты роста
• Стратегии развития

💡 Что вы получите:
• Практические кейсы
• Пошаговые инструкции
• Бесплатные материалы
• Экспертную поддержку

📚 Бесплатные материалы:
• Чек-лист "10 шагов к цифровизации"
• Гайд "Выбор CRM-системы"
• Шаблоны для автоматизации

🔗 Полезные ссылки:
• Группа участников: @digitalizacija_community
• Консультации: @biznes_consulting
• Советы: @automation_tips

💬 Задавайте вопросы в комментариях!

#цифровизация #бизнес #автоматизация #курс""",
                'type': 'channel'
            },
            
            'biznes_automation': {
                'title': '⚙️ Добро пожаловать в Biznes Automation!',
                'content': """🎯 Кейсы автоматизации бизнес-процессов

Здесь мы разбираем реальные примеры автоматизации:

🤖 Чат-боты для бизнеса
• Автоматизация продаж
• Поддержка клиентов
• Сбор заявок

📧 Email-маркетинг
• Автоматические воронки
• Сегментация аудитории
• A/B тестирование

📊 CRM и ERP системы
• Выбор подходящей системы
• Внедрение и настройка
• Интеграция с другими сервисами

🔄 Автоматизация рутинных задач
• Обработка документов
• Управление задачами
• Отчетность

📈 Инструменты для роста
• Аналитика и метрики
• Автоматизация рекламы
• Управление проектами

💼 Реальные кейсы:
• Как кафе автоматизировало заказы
• CRM для интернет-магазина
• Email-маркетинг для консалтинга

📋 Полезные материалы:
• Чек-листы по внедрению
• Гайды по настройке
• ROI от автоматизации

🔗 Дополнительно:
• Основной канал: @digitalizacija_biznesa
• Группа: @digitalizacija_community
• Консультации: @biznes_consulting

💬 Делитесь своими кейсами автоматизации!

#автоматизация #бизнес #кейсы #процессы""",
                'type': 'channel'
            },
            
            'startup_digital': {
                'title': '🚀 Добро пожаловать в Startup Digital!',
                'content': """🎯 Цифровизация для стартапов и предпринимателей

Здесь собрано все для цифрового бизнеса:

💡 Идеи для цифрового бизнеса
• SaaS-продукты
• Мобильные приложения
• Веб-платформы
• Цифровые сервисы

📱 Мобильные приложения
• MVP разработка
• Продвижение в App Store
• Монетизация
• Пользовательский опыт

🌐 Веб-платформы
• Выбор технологий
• UX/UI дизайн
• Разработка и запуск
• Масштабирование

📊 Аналитика стартапов
• Метрики роста
• Unit-экономика
• Воронка конверсии
• Продуктовая аналитика

💰 Привлечение инвестиций
• Подготовка pitch deck
• Финансовое моделирование
• Встречи с инвесторами
• Due diligence

🎯 Стратегии роста
• Product-market fit
• Горизонтальное масштабирование
• Международная экспансия
• Экзит-стратегии

📈 Метрики успеха
• CAC и LTV
• Churn rate
• NPS и удовлетворенность
• Время до окупаемости

🤝 Нетворкинг
• Сообщество предпринимателей
• Менторы и эксперты
• Партнерства
• Инвестиционные клубы

🔗 Полезные ресурсы:
• Основной канал: @digitalizacija_biznesa
• Автоматизация: @biznes_automation
• Группа: @digitalizacija_community

💬 Расскажите о своем стартапе!

#стартап #предпринимательство #цифровойбизнес #инвестиции""",
                'type': 'channel'
            },
            
            'digitalizacija_community': {
                'title': '👥 Добро пожаловать в Digitalizacija Community!',
                'content': """🎯 Основная группа участников курса "Digitalizacija Biznesa"

👋 Добро пожаловать в сообщество!

Здесь вы можете:

💬 Обсуждать темы курса
• Задавать вопросы
• Делиться опытом
• Получать поддержку

📚 Обмениваться материалами
• Полезные ссылки
• Инструменты
• Шаблоны и чек-листы

🤝 Нетворкинг
• Знакомиться с участниками
• Находить партнеров
• Обмениваться контактами

📊 Делиться результатами
• Кейсы внедрения
• Достижения
• Метрики и результаты

🎯 Получать помощь
• Консультации экспертов
• Ответы на вопросы
• Рекомендации

📈 Участвовать в мероприятиях
• Вебинары
• Мастер-классы
• Встречи сообщества

🔗 Наши каналы:
• Основной: @digitalizacija_biznesa
• Автоматизация: @biznes_automation
• Стартапы: @startup_digital

💡 Правила сообщества:
• Уважайте друг друга
• Делитесь полезным контентом
• Задавайте вопросы
• Помогайте новичкам

🚀 Вместе мы создаем будущее цифрового бизнеса!

#сообщество #цифровизация #бизнес #нетворкинг""",
                'type': 'group'
            },
            
            'biznes_consulting': {
                'title': '💼 Добро пожаловать в Biznes Consulting!',
                'content': """🎯 Группа консультаций по цифровизации бизнеса

Здесь вы можете получить персональную помощь:

👨‍💼 Консультации экспертов
• Аудит бизнес-процессов
• Рекомендации по автоматизации
• План цифровизации

📊 Анализ текущего состояния
• Оценка уровня цифровизации
• Выявление узких мест
• Определение приоритетов

💡 Подбор инструментов
• CRM-системы
• Инструменты автоматизации
• Аналитические платформы

📈 Расчет ROI
• Стоимость внедрения
• Ожидаемая экономия
• Сроки окупаемости

🚀 План внедрения
• Пошаговая стратегия
• Временные рамки
• Необходимые ресурсы

💼 Кейсы и примеры
• Реальные истории успеха
• Ошибки и их решения
• Лучшие практики

📞 Форматы консультаций:
• Персональные встречи
• Групповые сессии
• Онлайн-консультации
• Аудит документов

💰 Стоимость:
• Первая консультация: бесплатно
• Полный аудит: от $100
• Сопровождение: от $50/месяц

🔗 Записаться на консультацию:
• Напишите в группу
• Укажите тип бизнеса
• Опишите текущие задачи

💬 Задавайте вопросы и получайте экспертные ответы!

#консультации #аудит #цифровизация #эксперты""",
                'type': 'group'
            },
            
            'automation_tips': {
                'title': '💡 Добро пожаловать в Automation Tips!',
                'content': """🎯 Советы по автоматизации бизнеса

Здесь собраны практические советы и лайфхаки:

⚡ Быстрые решения
• Автоматизация за 5 минут
• Простые интеграции
• Бесплатные инструменты

🛠️ Инструменты и сервисы
• Обзоры новых платформ
• Сравнение решений
• Рекомендации по выбору

📋 Чек-листы и шаблоны
• Готовые алгоритмы
• Схемы процессов
• Шаблоны документов

🎯 Лайфхаки для бизнеса
• Экономия времени
• Снижение затрат
• Повышение эффективности

📊 Метрики и KPI
• Что измерять
• Как отслеживать
• Интерпретация данных

🔧 Технические решения
• API интеграции
• Автоматические скрипты
• Настройка систем

💡 Ежедневные советы
• Новые возможности
• Обновления инструментов
• Тренды автоматизации

📚 Образовательные материалы
• Мини-курсы
• Вебинары
• Полезные статьи

🤝 Обмен опытом
• Ваши лайфхаки
• Вопросы и ответы
• Совместные решения

🔗 Дополнительные ресурсы:
• Основной канал: @digitalizacija_biznesa
• Кейсы: @biznes_automation
• Сообщество: @digitalizacija_community

💬 Делитесь своими советами и лайфхаками!

#советы #лайфхаки #автоматизация #инструменты""",
                'type': 'group'
            }
        }
    
    def send_welcome_post(self, channel_key, chat_id):
        """Отправка приветственного поста в канал"""
        try:
            if channel_key not in self.welcome_posts:
                return {'status': 'error', 'message': f'Неизвестный канал: {channel_key}'}
            
            post_data = self.welcome_posts[channel_key]
            
            # Формируем полный текст поста
            full_text = f"{post_data['title']}\n\n{post_data['content']}"
            
            # Отправляем пост
            message = self.bot.send_message(
                chat_id=chat_id,
                text=full_text,
                parse_mode=None  # Отключаем Markdown для избежания ошибок
            )
            
            # Закрепляем пост
            try:
                self.bot.pin_chat_message(chat_id, message.message_id)
                print(f"   ✅ Пост закреплен")
            except Exception as e:
                print(f"   ⚠️ Не удалось закрепить пост: {e}")
            
            return {'status': 'success', 'message_id': message.message_id}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def pin_welcome_post(self, chat_id, message_id):
        """Закрепление поста"""
        try:
            self.bot.pin_chat_message(chat_id, message_id)
            return True
        except Exception as e:
            print(f"Ошибка закрепления поста: {e}")
            return False
    
    def send_all_welcome_posts(self, channel_ids):
        """Отправка приветственных постов во все каналы"""
        print("🚀 Отправка приветственных постов...")
        print("=" * 50)
        
        results = {}
        
        for channel_key, channel_data in channel_ids.items():
            if channel_key in self.welcome_posts:
                chat_id = channel_data.get('chat_id')
                if chat_id:
                    print(f"📝 Отправляем пост в {channel_key}...")
                    result = self.send_welcome_post(channel_key, chat_id)
                    results[channel_key] = result
                    
                    if result['status'] == 'success':
                        print(f"   ✅ Успешно отправлен")
                    else:
                        print(f"   ❌ Ошибка: {result['message']}")
                else:
                    print(f"   ⚠️ Нет ID канала для {channel_key}")
            else:
                print(f"   ⚠️ Нет шаблона поста для {channel_key}")
        
        # Сохраняем результаты
        self.save_results(results)
        
        return results
    
    def save_results(self, results):
        """Сохранение результатов отправки"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'welcome_posts_results_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📊 Результаты сохранены в {filename}")

def main():
    """Основная функция"""
    manager = WelcomePostsManager()
    
    # Загружаем ID каналов из .env
    channel_ids = {
        'digitalizacija_main': {
            'chat_id': os.getenv('DIGITALIZACIJA_MAIN_CHANNEL_ID'),
            'username': 'digitalizacija_biznesa'
        },
        'biznes_automation': {
            'chat_id': os.getenv('BIZNES_AUTOMATION_CHANNEL_ID'),
            'username': 'biznes_automation'
        },
        'startup_digital': {
            'chat_id': os.getenv('STARTUP_DIGITAL_CHANNEL_ID'),
            'username': 'startup_digital'
        },
        'digitalizacija_community': {
            'chat_id': os.getenv('DIGITALIZACIJA_COMMUNITY_ID'),
            'username': 'digitalizacija_community'
        },
        'biznes_consulting': {
            'chat_id': os.getenv('BIZNES_CONSULTING_ID'),
            'username': 'biznes_consulting'
        },
        'automation_tips': {
            'chat_id': os.getenv('AUTOMATION_TIPS_ID'),
            'username': 'automation_tips'
        }
    }
    
    # Отправляем посты
    results = manager.send_all_welcome_posts(channel_ids)
    
    # Показываем итоги
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    total_count = len(results)
    
    print(f"\n📊 ИТОГИ:")
    print(f"✅ Успешно: {success_count}/{total_count}")
    
    if success_count < total_count:
        print("❌ Есть ошибки. Проверьте права бота в каналах.")

if __name__ == "__main__":
    main() 