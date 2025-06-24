# 🚀 Быстрый запуск интегрированной системы

## Шаг 1: Подготовка

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Создайте файл .env в папке telegram_autopost_bot/
cd telegram_autopost_bot
echo "BOT_TOKEN=your_bot_token_here" > .env
echo "ADMIN_ID=your_admin_id_here" >> .env
cd ..
```

## Шаг 2: Запуск системы

### Вариант A: Автоматический запуск
```bash
python start_universal_bot_system.py
# Выберите режим 2 (API + бот в фоне)
```

### Вариант B: Ручной запуск
```bash
# Терминал 1: API сервер
python main_api.py

# Терминал 2: Бот (опционально)
cd telegram_autopost_bot
python universal_bot.py
```

## Шаг 3: Проверка работы

```bash
# Запустите тесты
python test_integration.py

# Откройте в браузере
http://localhost:5000
```

## Шаг 4: Вход в систему

- **Логин:** admin
- **Пароль:** admin123

## Доступные страницы

- **Дашборд:** http://localhost:5000/universal-bot
- **Кампании:** http://localhost:5000/universal-bot/campaigns
- **Посты:** http://localhost:5000/universal-bot/posts
- **Генератор:** http://localhost:5000/universal-bot/generator

## Возможные проблемы

### ❌ "Не удалось импортировать интеграцию с ботом"
- Проверьте наличие файла `telegram_autopost_bot/bot_integration.py`
- Убедитесь в правильности путей

### ❌ "Не удалось подключиться к API серверу"
- Убедитесь, что сервер запущен на порту 5000
- Проверьте, что нет конфликтов портов

### ❌ "Ошибка входа в систему"
- Проверьте логин/пароль: admin/admin123
- Убедитесь в правильности конфигурации в `config.py`

### ❌ "Бот не отвечает"
- Проверьте токен в файле `.env`
- Убедитесь в правильности ADMIN_ID
- Проверьте права бота в Telegram

## Режимы работы

### 🔧 Тестовый режим
- Работает без реального бота
- Использует тестовые данные
- Подходит для разработки и тестирования

### 🤖 Полная интеграция
- Подключение к реальному боту
- Работа с реальными данными
- Полная функциональность

## Быстрые команды

```bash
# Запуск только фронтенда
python main_api.py

# Запуск только бота
cd telegram_autopost_bot && python universal_bot.py

# Тестирование интеграции
python test_integration.py

# Просмотр логов
tail -f logs/api.log
```

## Структура файлов

```
online-classes/
├── main_api.py                    # API сервер
├── templates/                     # HTML шаблоны
│   ├── universal_bot_dashboard.html
│   ├── universal_bot_campaigns.html
│   ├── universal_bot_posts.html
│   └── universal_bot_generator.html
├── telegram_autopost_bot/
│   ├── universal_bot.py          # Основной бот
│   ├── bot_integration.py        # Модуль интеграции
│   ├── config.py                 # Конфигурация
│   ├── database.py               # База данных
│   └── .env                      # Переменные окружения
├── start_universal_bot_system.py # Скрипт запуска
└── test_integration.py           # Тесты
```

## Следующие шаги

1. **Настройка каналов** - отредактируйте `config.py`
2. **Создание кампаний** - через веб-интерфейс
3. **Генерация контента** - используйте генератор
4. **Планирование постов** - настройте расписание
5. **Мониторинг** - следите за статистикой

## Поддержка

- 📖 Полная документация: `README_INTEGRATION.md`
- 🧪 Тесты: `python test_integration.py`
- 🔧 Настройка: `telegram_autopost_bot/config.py`
- 📝 Логи: `logs/` и `telegram_autopost_bot/logs/` 