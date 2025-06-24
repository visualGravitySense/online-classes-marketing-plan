#!/usr/bin/env python3
"""
Скрипт для проверки настроек .env файла
"""

import os
from dotenv import load_dotenv

def check_env_settings():
    """Проверка настроек окружения"""
    print("🔍 ПРОВЕРКА НАСТРОЕК .ENV ФАЙЛА")
    print("=" * 50)
    
    # Загружаем .env файл
    load_dotenv()
    
    # Список обязательных переменных
    required_vars = [
        'BOT_TOKEN',
        'ADMIN_ID'
    ]
    
    # Список ID каналов
    channel_vars = [
        'DIGITALIZACIJA_MAIN_CHANNEL_ID',
        'BIZNES_AUTOMATION_CHANNEL_ID', 
        'STARTUP_DIGITAL_CHANNEL_ID',
        'DIGITALIZACIJA_COMMUNITY_ID',
        'BIZNES_CONSULTING_ID',
        'AUTOMATION_TIPS_ID'
    ]
    
    # Проверяем обязательные переменные
    print("\n📋 ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ:")
    missing_required = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var}: {'*' * 10} (настроено)")
        else:
            print(f"❌ {var}: НЕ НАСТРОЕНО")
            missing_required.append(var)
    
    # Проверяем ID каналов
    print("\n📺 ID КАНАЛОВ И ГРУПП:")
    missing_channels = []
    
    for var in channel_vars:
        value = os.getenv(var)
        if value and value != '-100xxxxxxxxx':
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: НЕ НАСТРОЕНО")
            missing_channels.append(var)
    
    # Проверяем дополнительные настройки
    print("\n⚙️ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ:")
    
    lead_token = os.getenv('LEAD_BOT_TOKEN')
    if lead_token and lead_token != 'your_bot_token_here':
        print(f"✅ LEAD_BOT_TOKEN: {'*' * 10} (настроено)")
    else:
        print(f"⚠️ LEAD_BOT_TOKEN: использует BOT_TOKEN")
    
    db_path = os.getenv('DATABASE_PATH', 'data/')
    reports_path = os.getenv('REPORTS_PATH', 'reports/')
    debug_mode = os.getenv('DEBUG_MODE', 'false')
    
    print(f"✅ DATABASE_PATH: {db_path}")
    print(f"✅ REPORTS_PATH: {reports_path}")
    print(f"✅ DEBUG_MODE: {debug_mode}")
    
    # Итоговая оценка
    print("\n📊 ИТОГОВАЯ ОЦЕНКА:")
    
    if not missing_required and not missing_channels:
        print("🎉 ВСЕ НАСТРОЙКИ ЗАПОЛНЕНЫ!")
        print("✅ Система готова к запуску")
        return True
    else:
        print("⚠️ ЕСТЬ НЕЗАПОЛНЕННЫЕ НАСТРОЙКИ:")
        
        if missing_required:
            print(f"❌ Обязательные: {', '.join(missing_required)}")
        
        if missing_channels:
            print(f"❌ Каналы: {', '.join(missing_channels)}")
        
        print("\n📝 ИНСТРУКЦИИ ПО НАСТРОЙКЕ:")
        
        if 'BOT_TOKEN' in missing_required:
            print("1. Получите токен бота у @BotFather")
            print("   - Отправьте /newbot")
            print("   - Следуйте инструкциям")
        
        if 'ADMIN_ID' in missing_required:
            print("2. Получите ваш Telegram ID")
            print("   - Найдите @userinfobot")
            print("   - Отправьте любое сообщение")
        
        if missing_channels:
            print("3. Создайте каналы и группы:")
            print("   - Создайте каналы в Telegram")
            print("   - Добавьте бота как администратора")
            print("   - Получите ID через getUpdates")
        
        return False

def show_setup_instructions():
    """Показать инструкции по настройке"""
    print("\n📖 ПОДРОБНЫЕ ИНСТРУКЦИИ ПО НАСТРОЙКЕ:")
    print("=" * 50)
    
    print("""
1. 🎯 ПОЛУЧЕНИЕ ТОКЕНА БОТА:
   - Откройте Telegram
   - Найдите @BotFather
   - Отправьте /newbot
   - Введите имя: "Digitalizacija Biznesa Bot"
   - Введите username: "digitalizacija_biznesa_bot"
   - Скопируйте полученный токен

2. 👤 ПОЛУЧЕНИЕ ВАШЕГО ID:
   - Найдите @userinfobot в Telegram
   - Отправьте любое сообщение
   - Скопируйте ваш ID

3. 📺 СОЗДАНИЕ КАНАЛОВ И ГРУПП:
   - Создайте каналы в Telegram
   - Добавьте бота как администратора
   - Отправьте /start в каждый канал
   - Перейдите по ссылке:
     https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   - Найдите "chat":{"id":-100xxxxxxxxx}

4. 📝 ЗАПОЛНЕНИЕ .ENV ФАЙЛА:
   - Откройте файл .env в редакторе
   - Замените все "your_xxx_here" на реальные значения
   - Сохраните файл

5. ✅ ПРОВЕРКА НАСТРОЕК:
   - Запустите: python check_env.py
   - Убедитесь, что все ✅ зеленые
    """)

if __name__ == "__main__":
    success = check_env_settings()
    
    if not success:
        show_setup_instructions()
    
    print("\n" + "=" * 50)
    print("🔧 Для получения помощи используйте:")
    print("python check_env.py") 