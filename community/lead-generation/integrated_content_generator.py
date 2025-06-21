#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интегрированный контент-генератор для UX/UI курса
Работает с существующей системой Telegram бота
"""

import json
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os

# Добавляем путь к существующей системе
sys.path.append('../telegram_autopost_bot')

try:
    from config import CHANNELS, POSTING_SCHEDULE
except ImportError:
    print("⚠️ Не удалось импортировать config.py. Используем базовые настройки.")
    CHANNELS = {
        'digoGraphickDesign': {
            'chat_id': '-1002091962525',
            'name': 'digoGraphickDesign',
            'active': True
        },
        'digoUI': {
            'chat_id': '-1002123538949',
            'name': 'digoUI',
            'active': True
        }
    }
    POSTING_SCHEDULE = {
        'monday': ['09:00', '14:00', '18:00'],
        'tuesday': ['10:00', '15:00', '19:00'],
        'wednesday': ['09:30', '14:30', '18:30'],
        'thursday': ['09:00', '14:00', '18:00'],
        'friday': ['10:00', '15:00', '19:00'],
        'saturday': ['11:00', '16:00'],
        'sunday': ['12:00', '17:00']
    }

class IntegratedContentGenerator:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """Инициализация интегрированного генератора контента"""
        self.api_base_url = api_base_url
        self.audiences = {
            "новички": {
                "pain_points": [
                    "Не знаю, с чего начать изучение UX/UI",
                    "Боюсь, что у меня нет таланта к дизайну",
                    "Сколько времени нужно, чтобы стать дизайнером?",
                    "Какие инструменты нужно изучать в первую очередь?",
                    "Как понять, подходит ли мне эта профессия?"
                ],
                "solutions": [
                    "Пошаговое обучение с нуля без предварительных знаний",
                    "Понятные объяснения сложных концепций",
                    "Мотивационная поддержка на протяжении курса",
                    "Помощь в выборе специализации",
                    "Практические проекты для понимания процесса"
                ],
                "benefits": [
                    "Создавать пользовательские интерфейсы с нуля",
                    "Проводить UX-исследования и аналитику",
                    "Работать в Figma на профессиональном уровне",
                    "Создавать интерактивные прототипы"
                ],
                "salary_range": "от $500 до $1200",
                "time_to_result": "3-6 месяцев",
                "tone": "поддерживающий, мотивирующий",
                "target_channels": ["digoGraphickDesign"]  # Основной канал для новичков
            },
            "junior": {
                "pain_points": [
                    "Не могу найти первую работу в IT",
                    "Мое портфолио не привлекает внимание HR",
                    "Не знаю, как правильно презентовать свои проекты",
                    "Боюсь собеседований - не знаю, что спрашивают",
                    "Как перейти от учебных проектов к реальным?"
                ],
                "solutions": [
                    "Портфолио, которое заметят работодатели",
                    "Подготовка к собеседованиям",
                    "Реальные кейсы для портфолио",
                    "Связи в IT-индустрии",
                    "Профессиональные навыки работы"
                ],
                "benefits": [
                    "Создавать проекты, которые привлекают HR",
                    "Правильно презентовать свои работы",
                    "Подготовиться к собеседованиям в IT",
                    "Найти связи в индустрии"
                ],
                "salary_range": "от $1200 до $2500",
                "time_to_result": "1-3 месяца",
                "tone": "профессиональный, уверенный",
                "target_channels": ["digoUI"]  # Специализированный канал для junior
            },
            "freelancers": {
                "pain_points": [
                    "Клиенты не готовы платить достойные деньги",
                    "Конкуренция на фрилансе слишком высокая",
                    "Не знаю, как правильно оценивать свои услуги",
                    "Как найти постоянных клиентов?",
                    "Боюсь, что не справлюсь с реальными проектами"
                ],
                "solutions": [
                    "Навыки, за которые платят больше",
                    "Стратегии ценообразования",
                    "Поиск и удержание клиентов",
                    "Управление проектами",
                    "Профессиональные стандарты качества"
                ],
                "benefits": [
                    "Создавать проекты премиум-качества",
                    "Правильно оценивать свои услуги",
                    "Находить и удерживать постоянных клиентов",
                    "Управлять проектами профессионально"
                ],
                "salary_range": "от $1500 за проект",
                "time_to_result": "2-4 месяца",
                "tone": "деловой, результативный",
                "target_channels": ["digoGraphickDesign", "digoUI"]  # Оба канала для фрилансеров
            },
            "developers": {
                "pain_points": [
                    "Не понимаю, что хотят дизайнеры",
                    "Как лучше коммуницировать с дизайн-командой?",
                    "Хочу понимать принципы UX/UI для лучшего кода",
                    "Как создать интерфейс, который понравится пользователям?",
                    "Нужны ли мне навыки дизайна для карьерного роста?"
                ],
                "solutions": [
                    "Общий язык с дизайнерами",
                    "Принципы UX/UI для лучшего кода",
                    "Инструменты для прототипирования",
                    "Понимание пользовательского опыта",
                    "Навыки для карьерного роста"
                ],
                "benefits": [
                    "Понимать принципы UX/UI для лучшего кода",
                    "Эффективно коммуницировать с дизайнерами",
                    "Создавать интерфейсы, которые нравятся пользователям",
                    "Использовать инструменты прототипирования"
                ],
                "salary_range": "дополнительно $500-1000",
                "time_to_result": "1-2 месяца",
                "tone": "технический, логичный",
                "target_channels": ["digoUI"]  # Технический канал для разработчиков
            }
        }
        
        self.cta_variants = {
            "мягкие": [
                "Хочешь узнать больше? Пиши в комментарии 👇",
                "Сохрани пост - пригодится! 💾",
                "Какие вопросы есть по теме? 🤔",
                "Делитесь опытом в комментариях 💬"
            ],
            "средние": [
                "Готов начать путь в UX/UI? Первый урок бесплатно 🚀",
                "Хочешь такой же результат? Записывайся на курс 📝",
                "Попробуй бесплатно - пойми, подходит ли тебе дизайн ✨",
                "Узнай больше о курсе - ссылка в профиле 🔗"
            ],
            "жесткие": [
                "Записывайся на курс прямо сейчас - места ограничены! 🔥",
                "Хватит откладывать! Начни зарабатывать в IT уже через 3 месяца 💰",
                "Только сегодня - скидка 50%! Успей записаться ⏰",
                "Осталось 5 мест в группе - торопись! 🎯"
            ]
        }
        
        self.success_stories = {
            "новички": [
                "Анна, бывший бухгалтер, теперь UX-дизайнер в IT-компании",
                "Дмитрий, студент, нашел работу через 2 месяца после курса"
            ],
            "junior": [
                "Михаил, junior-разработчик, получил повышение после изучения UX",
                "Елена, junior-дизайнер, устроилась в крупную IT-компанию"
            ],
            "freelancers": [
                "Елена, фрилансер, увеличила доход в 3 раза",
                "Алексей, фрилансер, нашел постоянных клиентов"
            ],
            "developers": [
                "Михаил, junior-разработчик, получил повышение после изучения UX",
                "Сергей, middle-разработчик, улучшил коммуникацию с дизайнерами"
            ]
        }

    def get_available_channels(self) -> List[Dict]:
        """Получить список доступных каналов"""
        return [
            {
                "name": channel_name,
                "chat_id": channel_data["chat_id"],
                "active": channel_data["active"]
            }
            for channel_name, channel_data in CHANNELS.items()
            if channel_data["active"]
        ]

    def get_next_posting_time(self, channel_name: str) -> datetime:
        """Получить следующее время для публикации в канале"""
        today = datetime.now()
        weekday = today.strftime('%A').lower()
        
        if weekday in POSTING_SCHEDULE:
            times = POSTING_SCHEDULE[weekday]
            for time_str in times:
                hour, minute = map(int, time_str.split(':'))
                posting_time = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if posting_time > today:
                    return posting_time
        
        # Если все время на сегодня прошло, берем первое время завтра
        tomorrow = today + timedelta(days=1)
        next_weekday = tomorrow.strftime('%A').lower()
        
        if next_weekday in POSTING_SCHEDULE:
            first_time = POSTING_SCHEDULE[next_weekday][0]
            hour, minute = map(int, first_time.split(':'))
            return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Fallback - через 2 часа
        return today + timedelta(hours=2)

    def generate_problem_solution_post(self, audience: str, cta_strength: str = "средние") -> Dict:
        """Генерация поста типа 'Проблема-Решение'"""
        audience_data = self.audiences[audience]
        
        pain_point = random.choice(audience_data["pain_points"])
        solution = random.choice(audience_data["solutions"])
        benefits = random.sample(audience_data["benefits"], 3)
        cta = random.choice(self.cta_variants[cta_strength])
        success_story = random.choice(self.success_stories[audience])
        
        title = f"{pain_point}? Вот как {audience} решают эту проблему за {audience_data['time_to_result']}"
        
        content = f"""Знакомая ситуация? "{pain_point}" - это то, с чем сталкивается каждый {audience}.

Ты тратишь часы на изучение, но результат все равно не радует. А все потому, что изучение UX/UI - это не просто "посмотреть видео и стать дизайнером".

{solution} - именно то, что нужно {audience}.

На нашем курсе ты научишься:
✅ {benefits[0]}
✅ {benefits[1]}
✅ {benefits[2]}

И самое главное - получишь реальный проект в портфолио, а не просто сертификат.

{success_story}.

Наши выпускники уже работают в IT-компаниях и зарабатывают {audience_data['salary_range']}.

{cta}

P.S. Первый урок бесплатно - попробуй и пойми, подходит ли тебе UX/UI дизайн."""
        
        return {
            "type": "проблема-решение",
            "audience": audience,
            "title": title,
            "content": content,
            "cta_strength": cta_strength,
            "generated_at": datetime.now().isoformat()
        }

    def generate_success_story_post(self, audience: str, cta_strength: str = "средние") -> Dict:
        """Генерация поста типа 'История успеха'"""
        audience_data = self.audiences[audience]
        success_story = random.choice(self.success_stories[audience])
        pain_point = random.choice(audience_data["pain_points"])
        benefits = random.sample(audience_data["benefits"], 3)
        cta = random.choice(self.cta_variants[cta_strength])
        
        title = f"От {audience} до UX-дизайнера за {audience_data['time_to_result']}. История успеха"
        
        content = f"""Знакомьтесь с {audience} - {success_story}.

"{pain_point}" - именно с этого начинался путь нашего студента.

"Я {audience}, но хотел большего. {pain_point} - это то, что меня останавливало.

Думал, что дизайн - это только для тех, кто умеет рисовать. Оказалось, что {audience_data['solutions'][0]}."

Наш курс дал {audience} именно то, что нужно:

{benefits[0]}
{benefits[1]}
{benefits[2]}

Сейчас {success_story} и зарабатывает {audience_data['salary_range']}.

"UX/UI дизайн - это не магия, а методология. Главное - начать с правильной базы."

{cta}

Твоя история успеха может быть следующей! 🚀"""
        
        return {
            "type": "история-успеха",
            "audience": audience,
            "title": title,
            "content": content,
            "cta_strength": cta_strength,
            "generated_at": datetime.now().isoformat()
        }

    def generate_educational_post(self, audience: str, tool: str = "Figma", cta_strength: str = "мягкие") -> Dict:
        """Генерация образовательного поста"""
        audience_data = self.audiences[audience]
        benefit = random.choice(audience_data["benefits"])
        pain_point = random.choice(audience_data["pain_points"])
        solution = random.choice(audience_data["solutions"])
        cta = random.choice(self.cta_variants[cta_strength])
        
        title = f"{tool}: {benefit} для {audience}"
        
        content = f"""{audience} часто спрашивают: "Как {benefit}?"

Сегодня разбираем {tool} - инструмент, который изменит твой подход к дизайну.

🎯 Что такое {tool}:
- {benefit}
- {audience_data['benefits'][0]}
- {audience_data['benefits'][1]}

🔧 Как использовать:
1. {audience_data['solutions'][0]}
2. {audience_data['solutions'][1]}
3. {audience_data['solutions'][2]}

💡 Практический совет:
"{pain_point}" - это частая ошибка {audience}. {solution} поможет избежать этой проблемы.

{tool} - это только один из инструментов, которые ты освоишь на курсе.

{cta}"""
        
        return {
            "type": "образовательный",
            "audience": audience,
            "tool": tool,
            "title": title,
            "content": content,
            "cta_strength": cta_strength,
            "generated_at": datetime.now().isoformat()
        }

    def generate_promo_post(self, audience: str, cta_strength: str = "жесткие") -> Dict:
        """Генерация промо-поста"""
        audience_data = self.audiences[audience]
        pain_point = random.choice(audience_data["pain_points"])
        benefits = random.sample(audience_data["benefits"], 4)
        success_story = random.choice(self.success_stories[audience])
        cta = random.choice(self.cta_variants[cta_strength])
        
        title = f"🚀 {audience}: {audience_data['benefits'][0]} за {audience_data['time_to_result']}"
        
        content = f""""{pain_point}" - знакомая проблема?

Наш курс создан специально для {audience}, которые хотят {audience_data['benefits'][0]}.

✅ {audience_data['solutions'][0]}
✅ {benefits[0]}
✅ {benefits[1]}
✅ {benefits[2]}
✅ Реальный проект в портфолио
✅ Поддержка после курса

{success_story}.

Наши выпускники работают в компаниях и зарабатывают {audience_data['salary_range']}.

🔥 Только до пятницы - скидка 30% + бонусный модуль

{cta}"""
        
        return {
            "type": "промо",
            "audience": audience,
            "title": title,
            "content": content,
            "cta_strength": cta_strength,
            "generated_at": datetime.now().isoformat()
        }

    def create_post_via_api(self, post_data: Dict, channel_id: str, scheduled_time: datetime) -> bool:
        """Создать пост через API"""
        try:
            api_url = f"{self.api_base_url}/api/posts"
            
            payload = {
                "content": post_data["content"],
                "channel_id": channel_id,
                "scheduled_time": scheduled_time.isoformat(),
                "media_path": None,
                "media_type": None
            }
            
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ Пост создан успешно для канала {channel_id}")
                return True
            else:
                print(f"❌ Ошибка создания поста: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при отправке запроса: {str(e)}")
            return False

    def auto_schedule_content(self, audience: str, post_type: str = "проблема-решение", 
                            cta_strength: str = "средние", days_ahead: int = 7) -> List[Dict]:
        """Автоматическое планирование контента для аудитории"""
        audience_data = self.audiences[audience]
        target_channels = audience_data["target_channels"]
        
        scheduled_posts = []
        
        for channel_name in target_channels:
            if channel_name not in CHANNELS:
                print(f"⚠️ Канал {channel_name} не найден в конфигурации")
                continue
                
            channel_id = CHANNELS[channel_name]["chat_id"]
            
            # Генерируем посты на указанное количество дней вперед
            for day in range(days_ahead):
                # Генерируем контент
                if post_type == "проблема-решение":
                    post_data = self.generate_problem_solution_post(audience, cta_strength)
                elif post_type == "история-успеха":
                    post_data = self.generate_success_story_post(audience, cta_strength)
                elif post_type == "образовательный":
                    post_data = self.generate_educational_post(audience, "Figma", cta_strength)
                elif post_type == "промо":
                    post_data = self.generate_promo_post(audience, cta_strength)
                else:
                    post_data = self.generate_problem_solution_post(audience, cta_strength)
                
                # Получаем время для публикации
                scheduled_time = self.get_next_posting_time(channel_name)
                scheduled_time += timedelta(days=day)
                
                # Создаем пост через API
                success = self.create_post_via_api(post_data, channel_id, scheduled_time)
                
                if success:
                    scheduled_posts.append({
                        "post_data": post_data,
                        "channel_id": channel_id,
                        "channel_name": channel_name,
                        "scheduled_time": scheduled_time,
                        "status": "scheduled"
                    })
        
        return scheduled_posts

    def generate_and_preview(self, audience: str, post_type: str = "проблема-решение", 
                           cta_strength: str = "средние") -> Dict:
        """Генерировать контент для предпросмотра"""
        if post_type == "проблема-решение":
            post_data = self.generate_problem_solution_post(audience, cta_strength)
        elif post_type == "история-успеха":
            post_data = self.generate_success_story_post(audience, cta_strength)
        elif post_type == "образовательный":
            post_data = self.generate_educational_post(audience, "Figma", cta_strength)
        elif post_type == "промо":
            post_data = self.generate_promo_post(audience, cta_strength)
        else:
            post_data = self.generate_problem_solution_post(audience, cta_strength)
        
        return {
            "post_data": post_data,
            "available_channels": self.get_available_channels(),
            "next_posting_times": {
                channel["name"]: self.get_next_posting_time(channel["name"])
                for channel in self.get_available_channels()
            }
        }

def main():
    """Демонстрация работы интегрированного генератора"""
    generator = IntegratedContentGenerator()
    
    print("🎯 Интегрированный генератор контента для UX/UI курса")
    print("=" * 60)
    
    # Показываем доступные каналы
    print("\n📢 Доступные каналы:")
    channels = generator.get_available_channels()
    for channel in channels:
        print(f"  - {channel['name']} ({channel['chat_id']})")
    
    # Демонстрируем генерацию контента
    print("\n📝 Генерация контента для предпросмотра:")
    preview = generator.generate_and_preview("новички", "проблема-решение", "средние")
    
    print(f"Аудитория: {preview['post_data']['audience']}")
    print(f"Тип поста: {preview['post_data']['type']}")
    print(f"CTA: {preview['post_data']['cta_strength']}")
    print(f"\nЗаголовок: {preview['post_data']['title']}")
    print(f"\nКонтент:\n{preview['post_data']['content']}")
    
    # Показываем следующее время публикации
    print("\n⏰ Следующее время публикации:")
    for channel_name, posting_time in preview['next_posting_times'].items():
        print(f"  - {channel_name}: {posting_time.strftime('%d.%m.%Y %H:%M')}")
    
    # Спрашиваем о планировании
    print("\n" + "=" * 60)
    response = input("Хотите запланировать контент автоматически? (y/n): ")
    
    if response.lower() == 'y':
        audience = input("Выберите аудиторию (новички/junior/freelancers/developers): ")
        post_type = input("Выберите тип поста (проблема-решение/история-успеха/образовательный/промо): ")
        days = int(input("На сколько дней вперед планировать? (1-30): "))
        
        print(f"\n🚀 Планируем контент для {audience} на {days} дней...")
        scheduled = generator.auto_schedule_content(audience, post_type, "средние", days)
        
        print(f"✅ Запланировано {len(scheduled)} постов")
        for post in scheduled:
            print(f"  - {post['channel_name']}: {post['scheduled_time'].strftime('%d.%m.%Y %H:%M')}")

if __name__ == "__main__":
    main() 