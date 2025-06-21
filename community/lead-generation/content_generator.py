#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Контент-генератор для UX/UI курса
Автоматизированная система создания постов для 4 целевых аудиторий
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class ContentGenerator:
    def __init__(self):
        """Инициализация генератора контента"""
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
                "tone": "поддерживающий, мотивирующий"
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
                "tone": "профессиональный, уверенный"
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
                "tone": "деловой, результативный"
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
                "tone": "технический, логичный"
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

    def generate_content_batch(self, post_types: List[str] = None, audiences: List[str] = None, 
                             cta_strength: str = "средние") -> List[Dict]:
        """Генерация батча постов"""
        if post_types is None:
            post_types = ["проблема-решение", "история-успеха", "образовательный", "промо"]
        
        if audiences is None:
            audiences = list(self.audiences.keys())
        
        posts = []
        
        for audience in audiences:
            for post_type in post_types:
                if post_type == "проблема-решение":
                    post = self.generate_problem_solution_post(audience, cta_strength)
                elif post_type == "история-успеха":
                    post = self.generate_success_story_post(audience, cta_strength)
                elif post_type == "образовательный":
                    post = self.generate_educational_post(audience, "Figma", cta_strength)
                elif post_type == "промо":
                    post = self.generate_promo_post(audience, cta_strength)
                
                posts.append(post)
        
        return posts

    def export_to_telegram_format(self, posts: List[Dict]) -> str:
        """Экспорт постов в формат для Telegram"""
        telegram_posts = []
        
        for i, post in enumerate(posts, 1):
            telegram_post = f"""📝 ПОСТ #{i} - {post['type'].upper()}
🎯 АУДИТОРИЯ: {post['audience']}
📊 CTA: {post['cta_strength']}

📌 ЗАГОЛОВОК:
{post['title']}

📱 КОНТЕНТ:
{post['content']}

---
"""
            telegram_posts.append(telegram_post)
        
        return "\n".join(telegram_posts)

    def save_to_json(self, posts: List[Dict], filename: str = None) -> str:
        """Сохранение постов в JSON файл"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_content_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """Основная функция для демонстрации работы генератора"""
    generator = ContentGenerator()
    
    print("🎯 Генератор контента для UX/UI курса")
    print("=" * 50)
    
    # Генерируем примеры постов для каждой аудитории
    audiences = ["новички", "junior", "freelancers", "developers"]
    
    for audience in audiences:
        print(f"\n📝 Генерируем контент для аудитории: {audience}")
        print("-" * 40)
        
        # Проблема-решение пост
        post = generator.generate_problem_solution_post(audience, "средние")
        print(f"Заголовок: {post['title']}")
        print(f"Тип: {post['type']}")
        print(f"CTA: {post['cta_strength']}")
        print()
    
    # Генерируем полный батч
    print("\n🚀 Генерируем полный батч постов...")
    batch = generator.generate_content_batch()
    
    # Сохраняем в JSON
    filename = generator.save_to_json(batch)
    print(f"✅ Сохранено в файл: {filename}")
    
    # Экспортируем для Telegram
    telegram_content = generator.export_to_telegram_format(batch[:4])  # Первые 4 поста
    print(f"\n📱 Telegram формат (первые 4 поста):")
    print("=" * 50)
    print(telegram_content)

if __name__ == "__main__":
    main() 