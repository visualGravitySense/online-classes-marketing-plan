import random
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import requests

class ContentGenerator:
    def __init__(self):
        self.audience_matrix = {
            "Новички в дизайне": {
                "problems": [
                    "Не знаю с чего начать изучение дизайна",
                    "Боюсь что у меня нет таланта к дизайну",
                    "Не понимаю как создавать красивые интерфейсы",
                    "Запутался в огромном количестве инструментов",
                    "Не знаю какую нишу выбрать"
                ],
                "solutions": [
                    "Пошаговое обучение от основ до продвинутых техник",
                    "Практические проекты для портфолио",
                    "Современные инструменты и технологии",
                    "Поддержка ментора на каждом этапе",
                    "Готовые шаблоны и ресурсы"
                ],
                "benefits": [
                    "Создашь первое портфолио за 3 недели",
                    "Научишься работать в Figma и других инструментах",
                    "Поймешь принципы UX/UI дизайна",
                    "Получишь готовые проекты для резюме",
                    "Начнешь зарабатывать на дизайне"
                ]
            },
            "Junior дизайнеры": {
                "problems": [
                    "Не могу найти первую работу",
                    "Портфолио выглядит слабо",
                    "Не понимаю что хотят работодатели",
                    "Боюсь собеседований",
                    "Не знаю как расти дальше"
                ],
                "solutions": [
                    "Создание сильного портфолио",
                    "Подготовка к собеседованиям",
                    "Изучение требований рынка",
                    "Разбор реальных кейсов",
                    "Стратегия карьерного роста"
                ],
                "benefits": [
                    "Получишь предложения о работе",
                    "Увеличишь зарплату в 2-3 раза",
                    "Научишься презентовать себя",
                    "Поймешь тренды индустрии",
                    "Построишь карьерную стратегию"
                ]
            },
            "Фрилансеры": {
                "problems": [
                    "Не могу найти клиентов",
                    "Низкие цены на проекты",
                    "Нестабильный доход",
                    "Сложно оценивать проекты",
                    "Конкуренция с дешевыми исполнителями"
                ],
                "solutions": [
                    "Стратегии привлечения клиентов",
                    "Правильная оценка проектов",
                    "Создание личного бренда",
                    "Работа с премиум-клиентами",
                    "Автоматизация процессов"
                ],
                "benefits": [
                    "Увеличишь доход в 3-5 раз",
                    "Найдешь постоянных клиентов",
                    "Научишься продавать себя",
                    "Создашь стабильный поток заказов",
                    "Выйдешь на международный рынок"
                ]
            },
            "Разработчики": {
                "problems": [
                    "Не понимаю дизайн-процессы",
                    "Сложно работать с дизайнерами",
                    "Не умею создавать интерфейсы",
                    "Хочу делать full-stack проекты",
                    "Нужны навыки дизайна для роста"
                ],
                "solutions": [
                    "Изучение UX/UI принципов",
                    "Инструменты дизайна для разработчиков",
                    "Создание собственных интерфейсов",
                    "Интеграция дизайна и разработки",
                    "Full-stack подход к проектам"
                ],
                "benefits": [
                    "Станете full-stack специалистом",
                    "Увеличите стоимость услуг",
                    "Сможете создавать проекты под ключ",
                    "Лучше поймете дизайн-процессы",
                    "Откроете новые карьерные возможности"
                ]
            }
        }
        
        self.content_blocks = {
            "Проблема": [
                "🔥 {problem}\n\nЗнакомо? Большинство {audience} сталкиваются с этим каждый день.",
                "💡 {problem}\n\nЕсли это про вас - вы не одиноки!",
                "🎯 {problem}\n\nЭто главная боль {audience} в 2024 году.",
                "⚡ {problem}\n\nПора решить эту проблему раз и навсегда!"
            ],
            "Решение": [
                "✅ Решение: {solution}\n\nИменно этому мы учим в нашем курсе!",
                "🚀 {solution}\n\nЭто ключ к успеху в дизайне!",
                "💪 {solution}\n\nПроверенный метод, который работает!",
                "🎨 {solution}\n\nПростой способ достичь результата!"
            ],
            "Преимущества курса": [
                "🎓 Что вы получите:\n• {benefit1}\n• {benefit2}\n• {benefit3}\n\nГотовы начать?",
                "📈 Ваши результаты после курса:\n✅ {benefit1}\n✅ {benefit2}\n✅ {benefit3}",
                "🏆 На курсе вы научитесь:\n• {benefit1}\n• {benefit2}\n• {benefit3}",
                "💎 Главные преимущества:\n🔥 {benefit1}\n🔥 {benefit2}\n🔥 {benefit3}"
            ],
            "Кейс": [
                "📊 Кейс: {audience}\n\nДо курса: {problem}\nПосле курса: {benefit1}\n\nРезультат: {benefit2}",
                "🎯 История успеха:\n\n{audience} → {problem} → {solution} → {benefit1}",
                "📈 Реальный результат:\n\n{audience} добились {benefit1} за 3 недели!",
                "🏆 Успешный кейс:\n\n{audience} изменили карьеру: {problem} → {benefit1}"
            ],
            "Совет": [
                "💡 Совет для {audience}:\n\n{solution}\n\nЭто работает в 90% случаев!",
                "🎯 Важный совет:\n\n{solution}\n\nПримените это сегодня!",
                "⚡ Быстрый совет:\n\n{solution}\n\nРезультат не заставит ждать!",
                "🔑 Ключевой совет:\n\n{solution}\n\nЭто изменит ваш подход к дизайну!"
            ],
            "Мотивация": [
                "🚀 {audience}, пора действовать!\n\n{solution}\n\nВаш успех ждет вас!",
                "💪 Время перемен!\n\n{solution}\n\nВы способны на большее!",
                "🎯 Ваша цель достижима!\n\n{solution}\n\nНачните прямо сейчас!",
                "🔥 Не откладывайте на завтра!\n\n{solution}\n\nВаше будущее в ваших руках!"
            ]
        }
        
        self.cta_variations = [
            "👉 Начать обучение: @your_bot",
            "🎓 Записаться на курс: @your_bot", 
            "💎 Получить доступ: @your_bot",
            "🚀 Присоединиться: @your_bot",
            "📚 Узнать больше: @your_bot"
        ]

    def generate_content(self, audience_group: str, content_type: str, custom_prompt: Optional[str] = None) -> str:
        """Генерирует контент для указанной аудитории и типа"""
        
        if audience_group not in self.audience_matrix:
            raise ValueError(f"Неизвестная группа аудитории: {audience_group}")
            
        if content_type not in self.content_blocks:
            raise ValueError(f"Неизвестный тип контента: {content_type}")
        
        audience_data = self.audience_matrix[audience_group]
        
        # Выбираем случайные элементы
        problem = random.choice(audience_data["problems"])
        solution = random.choice(audience_data["solutions"])
        benefits = random.sample(audience_data["benefits"], 3)
        
        # Выбираем шаблон
        template = random.choice(self.content_blocks[content_type])
        
        # Заполняем шаблон
        content = template.format(
            audience=audience_group,
            problem=problem,
            solution=solution,
            benefit1=benefits[0],
            benefit2=benefits[1],
            benefit3=benefits[2]
        )
        
        # Добавляем CTA
        cta = random.choice(self.cta_variations)
        content += f"\n\n{cta}"
        
        return content

    def generate_batch(self, audience_group: str, count: int = 5) -> List[str]:
        """Генерирует пакет контента для аудитории"""
        content_types = list(self.content_blocks.keys())
        posts = []
        
        for _ in range(count):
            content_type = random.choice(content_types)
            post = self.generate_content(audience_group, content_type)
            posts.append(post)
            
        return posts

    def send_to_bot(self, content: str, channel_id: str, scheduled_time: Optional[datetime] = None) -> bool:
        """Отправляет контент через API бота"""
        try:
            api_url = "http://localhost:8000/api/posts"
            
            post_data = {
                "content": content,
                "channel_id": channel_id,
                "scheduled_time": scheduled_time.isoformat() if scheduled_time else datetime.now().isoformat(),
                "media_path": None,
                "media_type": None
            }
            
            response = requests.post(api_url, json=post_data)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Ошибка отправки в бот: {e}")
            return False

    def schedule_posts(self, audience_group: str, channel_id: str, posts_count: int = 10, 
                      start_time: Optional[datetime] = None, interval_hours: int = 24) -> List[bool]:
        """Планирует серию постов"""
        if not start_time:
            start_time = datetime.now() + timedelta(hours=1)
            
        posts = self.generate_batch(audience_group, posts_count)
        results = []
        
        for i, post in enumerate(posts):
            scheduled_time = start_time + timedelta(hours=i * interval_hours)
            success = self.send_to_bot(post, channel_id, scheduled_time)
            results.append(success)
            
        return results

# Пример использования
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Генерируем один пост
    post = generator.generate_content("Новички в дизайне", "Проблема")
    print("Сгенерированный пост:")
    print(post)
    print("\n" + "="*50 + "\n")
    
    # Генерируем пакет постов
    posts = generator.generate_batch("Junior дизайнеры", 3)
    print("Пакет постов:")
    for i, post in enumerate(posts, 1):
        print(f"Пост {i}:")
        print(post)
        print() 