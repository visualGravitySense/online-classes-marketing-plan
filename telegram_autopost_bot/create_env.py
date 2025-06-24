#!/usr/bin/env python3
"""
Скрипт для создания .env файла с существующими настройками и новыми каналами
"""

def create_env_file():
    """Создание .env файла"""
    
    env_content = """# ========================================
# НАСТРОЙКИ БОТА TELEGRAM
# ========================================

# Токен вашего бота (уже настроен)
BOT_TOKEN=your_existing_bot_token_here

# ID администратора (уже настроен)
ADMIN_ID=your_existing_admin_id_here

# ========================================
# СУЩЕСТВУЮЩИЕ КАНАЛЫ (уже настроены)
# ========================================

# Основной канал
MAIN_CHANNEL_ID=your_main_channel_id

# Тестовый канал
TEST_CHANNEL_ID=your_test_channel_id

# ========================================
# НОВЫЕ КАНАЛЫ ДЛЯ 'DIGITALIZACIJA BIZNESA'
# ========================================

# Основной канал кампании
DIGITALIZACIJA_MAIN_CHANNEL_ID=-100xxxxxxxxx

# Канал с кейсами автоматизации
BIZNES_AUTOMATION_CHANNEL_ID=-100xxxxxxxxx

# Канал для стартапов
STARTUP_DIGITAL_CHANNEL_ID=-100xxxxxxxxx

# Основная группа сообщества
DIGITALIZACIJA_COMMUNITY_ID=-100xxxxxxxxx

# Группа консультаций
BIZNES_CONSULTING_ID=-100xxxxxxxxx

# Группа с советами по автоматизации
AUTOMATION_TIPS_ID=-100xxxxxxxxx

# ========================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ========================================

# Токен для бота лидогенерации (может быть тот же)
LEAD_BOT_TOKEN=your_existing_bot_token_here

# Настройки базы данных
DATABASE_PATH=data/
REPORTS_PATH=reports/
DEBUG_MODE=false
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Файл .env создан!")
    print("\n📝 ИНСТРУКЦИИ ПО ЗАПОЛНЕНИЮ:")
    print("1. Замените 'your_existing_bot_token_here' на ваш токен бота")
    print("2. Замените 'your_existing_admin_id_here' на ваш Telegram ID")
    print("3. Замените 'your_main_channel_id' и 'your_test_channel_id' на ID существующих каналов")
    print("4. Замените '-100xxxxxxxxx' на ID новых каналов для кампании 'Digitalizacija Biznesa'")
    print("\n🔧 Для проверки настроек запустите:")
    print("python check_env.py")

if __name__ == "__main__":
    create_env_file() 