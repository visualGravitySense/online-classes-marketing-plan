import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

# Существующие каналы
CHANNELS = {
    'main': {
        'chat_id': os.getenv('MAIN_CHANNEL_ID'),
        'name': 'Main Channel',
        'active': True
    },
    'test': {
        'chat_id': os.getenv('TEST_CHANNEL_ID'),
        'name': 'Test Channel',
        'active': True
    },
    'designer_lfe': {
        'chat_id': '-1001903756368',
        'name': 'designer_lfe',
        'active': True,
        'target_audience': 'Designers',
        'description': 'Жизнь Дизайнера - сообщество для графических дизайнеров'
    },
    'digo_online_schools': {
        'chat_id': '-1002316535443',
        'name': 'digo_online_schools',
        'active': True,
        'target_audience': 'Developers',
        'description': 'Product Design & ML - для разработчиков и IT-специалистов'
    },
    'digoGraphickDesign': {
        'chat_id': '-1002091962525',
        'name': 'digoGraphickDesign',
        'active': True,
        'target_audience': 'Freelancers',
        'description': 'Сообщество фрилансеров и самоучек'
    },
    'digoUI': {
        'chat_id': '-1002123538949',
        'name': 'digoUI',
        'active': True,
        'target_audience': 'Juniors',
        'description': 'UX/UI для новичков и джуниоров'
    }
}

# Новые каналы для кампании "Digitalizacija Biznesa"
DIGITALIZACIJA_CHANNELS = {
    'digitalizacija_main': {
        'chat_id': os.getenv('DIGITALIZACIJA_MAIN_CHANNEL_ID'),
        'name': 'Digitalizacija Biznesa',
        'active': True,
        'target_audience': 'Business Owners',
        'description': 'Основной канал курса по цифровизации бизнеса',
        'campaign': 'digitalizacija'
    },
    'biznes_automation': {
        'chat_id': os.getenv('BIZNES_AUTOMATION_CHANNEL_ID'),
        'name': 'Biznes Automation',
        'active': True,
        'target_audience': 'Managers',
        'description': 'Кейсы автоматизации бизнес-процессов',
        'campaign': 'digitalizacija'
    },
    'startup_digital': {
        'chat_id': os.getenv('STARTUP_DIGITAL_CHANNEL_ID'),
        'name': 'Startup Digital',
        'active': True,
        'target_audience': 'Entrepreneurs',
        'description': 'Цифровизация для стартапов и предпринимателей',
        'campaign': 'digitalizacija'
    },
    'digitalizacija_community': {
        'chat_id': os.getenv('DIGITALIZACIJA_COMMUNITY_ID'),
        'name': 'Digitalizacija Community',
        'active': True,
        'target_audience': 'All',
        'description': 'Основная группа участников курса',
        'campaign': 'digitalizacija',
        'type': 'group'
    },
    'biznes_consulting': {
        'chat_id': os.getenv('BIZNES_CONSULTING_ID'),
        'name': 'Biznes Consulting',
        'active': True,
        'target_audience': 'Consultants',
        'description': 'Группа консультаций по цифровизации',
        'campaign': 'digitalizacija',
        'type': 'group'
    },
    'automation_tips': {
        'chat_id': os.getenv('AUTOMATION_TIPS_ID'),
        'name': 'Automation Tips',
        'active': True,
        'target_audience': 'All',
        'description': 'Советы по автоматизации бизнеса',
        'campaign': 'digitalizacija',
        'type': 'group'
    }
}

# Объединяем все каналы
ALL_CHANNELS = {**CHANNELS, **DIGITALIZACIJA_CHANNELS}

DATABASE_URL = os.getenv('DATABASE_URL', 'data/posts.db')

# Расписание публикаций для разных кампаний
POSTING_SCHEDULE = {
    'default': {
        'monday': ['09:00', '14:00', '18:00'],
        'tuesday': ['10:00', '15:00', '19:00'],
        'wednesday': ['09:30', '14:30', '18:30'],
        'thursday': ['09:00', '14:00', '18:00'],
        'friday': ['10:00', '15:00', '19:00'],
        'saturday': ['11:00', '16:00'],
        'sunday': ['12:00', '17:00']
    },
    'digitalizacija': {
        'monday': ['09:00', '12:00', '18:00', '21:00'],
        'tuesday': ['09:00', '12:00', '18:00', '21:00'],
        'wednesday': ['09:00', '12:00', '18:00', '21:00'],
        'thursday': ['09:00', '12:00', '18:00', '21:00'],
        'friday': ['09:00', '12:00', '18:00', '21:00'],
        'saturday': ['11:00', '15:00', '19:00'],
        'sunday': ['11:00', '15:00', '19:00']
    }
}

# Шаблоны постов для разных кампаний
POST_TEMPLATES = {
    'default': {
        'educational': """
💡 UX/UI Совет дня

{content}

🔖 Сохраняй пост, чтобы не потерять!
💬 Делись своим мнением в комментариях

#UXUITips #Дизайн #Обучение
""",
        
        'case_study': """
📊 Разбор интерфейса

{content}

❓ Как бы вы решили эту задачу?
👆 Ставь лайк, если пост полезен!

#Кейс #UXDesign #Интерфейс
""",
        
        'promo': """
🚀 {content}

📞 Узнать подробности: {link}
💌 Есть вопросы? Пиши в ЛС!

#Курс #UXUIДизайн #Обучение
"""
    },
    'digitalizacija': {
        'educational': """
🎯 {title}

📝 {content}

💡 Практический совет: {tip}

📊 {statistic}

❓ {question}

#цифровизация #бизнес #автоматизация
""",
        
        'problem': """
⚠️ {title}

😰 {problem_description}

💔 {consequences}

🔍 {diagnosis}

✅ {solution}

🚀 {call_to_action}

#проблемыбизнеса #решения #цифровизация
""",
        
        'selling': """
🎯 {title}

💡 {problem}

✅ {advantages}

📈 {results}

🎁 {bonuses}

⏰ {limitation}

💳 {call_to_action}

#курс #цифровизация #обучение
""",
        
        'case_study': """
📊 Кейс: {title}

🏢 {company_description}

😰 Проблема: {problem}

✅ Решение: {solution}

📈 Результат: {results}

💡 Выводы: {conclusions}

#кейс #цифровизация #бизнес
"""
    }
} 