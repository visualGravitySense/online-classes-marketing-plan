import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
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
DATABASE_URL = os.getenv('DATABASE_URL', 'data/posts.db')

# Posting schedule
POSTING_SCHEDULE = {
    'monday': ['09:00', '14:00', '18:00'],
    'tuesday': ['10:00', '15:00', '19:00'],
    'wednesday': ['09:30', '14:30', '18:30'],
    'thursday': ['09:00', '14:00', '18:00'],
    'friday': ['10:00', '15:00', '19:00'],
    'saturday': ['11:00', '16:00'],
    'sunday': ['12:00', '17:00']
}

# Post templates
POST_TEMPLATES = {
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
} 