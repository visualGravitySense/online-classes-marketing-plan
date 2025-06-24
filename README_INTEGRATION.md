# Интеграция фронтенда с универсальным ботом

## Обзор

Данный документ описывает процесс интеграции HTML фронтенда с реальным универсальным Telegram ботом.

## Структура интеграции

### Компоненты системы

1. **API сервер** (`main_api.py`) - Flask приложение с фронтендом
2. **Универсальный бот** (`telegram_autopost_bot/universal_bot.py`) - Telegram бот
3. **Модуль интеграции** (`telegram_autopost_bot/bot_integration.py`) - связующее звено
4. **База данных** (`telegram_autopost_bot/data/posts.db`) - SQLite база данных
5. **Конфигурация** (`telegram_autopost_bot/config.py`) - настройки бота

### Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Server     │    │  Bot Integration│
│   (HTML/CSS/JS) │◄──►│   (Flask)        │◄──►│   (Python)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Database       │    │  Universal Bot  │
                       │   (SQLite)       │    │  (Telegram)     │
                       └──────────────────┘    └─────────────────┘
```

## Установка и настройка

### 1. Подготовка окружения

```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание необходимых папок
mkdir -p telegram_autopost_bot/data
mkdir -p data
```

### 2. Настройка конфигурации

Создайте файл `telegram_autopost_bot/.env`:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here

# Channel IDs (опционально)
MAIN_CHANNEL_ID=-1001234567890
TEST_CHANNEL_ID=-1001234567891
DIGITALIZACIJA_MAIN_CHANNEL_ID=-1001234567892
BIZNES_AUTOMATION_CHANNEL_ID=-1001234567893
STARTUP_DIGITAL_CHANNEL_ID=-1001234567894
DIGITALIZACIJA_COMMUNITY_ID=-1001234567895
BIZNES_CONSULTING_ID=-1001234567896
AUTOMATION_TIPS_ID=-1001234567897
```

### 3. Настройка каналов

Отредактируйте `telegram_autopost_bot/config.py` для настройки ваших каналов:

```python
# Пример настройки каналов
CHANNELS = {
    'your_channel': {
        'chat_id': '-1001234567890',
        'name': 'Your Channel Name',
        'active': True,
        'campaign': 'default'  # или 'digitalizacija'
    }
}
```

## Запуск системы

### Автоматический запуск

Используйте скрипт для запуска всей системы:

```bash
python start_universal_bot_system.py
```

Выберите режим запуска:
1. **Только API сервер** - для работы с фронтендом
2. **API + бот в фоне** - полная система
3. **Только бот** - для работы через Telegram
4. **Полная система** - API + бот

### Ручной запуск

#### Запуск API сервера:
```bash
python main_api.py
```

#### Запуск бота:
```bash
cd telegram_autopost_bot
python universal_bot.py
```

## Интеграционные возможности

### 1. Управление кампаниями

**API эндпоинты:**
- `GET /api/universal-bot/campaigns` - получение списка кампаний
- `POST /api/universal-bot/campaigns` - создание кампании
- `POST /api/universal-bot/campaigns/{id}/start` - запуск кампании
- `POST /api/universal-bot/campaigns/{id}/pause` - приостановка кампании
- `DELETE /api/universal-bot/campaigns/{id}` - удаление кампании

**Интеграция с ботом:**
- Автоматическое получение кампаний из конфигурации
- Управление статусом планировщиков
- Синхронизация с реальными каналами

### 2. Управление постами

**API эндпоинты:**
- `GET /api/universal-bot/posts` - получение списка постов
- `POST /api/universal-bot/posts` - создание поста
- `DELETE /api/universal-bot/posts/{id}` - удаление поста

**Интеграция с ботом:**
- Сохранение постов в реальную базу данных
- Планирование публикаций
- Отслеживание статуса публикаций

### 3. Генерация контента

**API эндпоинты:**
- `POST /api/universal-bot/generate-content` - генерация контента

**Интеграция с ботом:**
- Использование реального генератора контента
- Поддержка различных тонов и стилей
- Автоматическое добавление хештегов

### 4. Аналитика и мониторинг

**API эндпоинты:**
- `GET /api/universal-bot/dashboard` - данные дашборда
- `GET /api/universal-bot/system-status` - статус системы

**Интеграция с ботом:**
- Реальная статистика по кампаниям
- Мониторинг статуса компонентов
- Отслеживание производительности

## Модели данных

### BotCampaign
```python
@dataclass
class BotCampaign:
    id: str
    name: str
    description: str
    status: str  # 'active', 'inactive', 'paused'
    channels: List[Dict]
    posts_count: int
    scheduled_posts: int
    created_at: str
    updated_at: str
```

### BotChannel
```python
@dataclass
class BotChannel:
    id: str
    name: str
    chat_id: str
    campaign: str
    status: str  # 'active', 'inactive'
    posts_count: int
    last_post_date: Optional[str]
```

### BotPost
```python
@dataclass
class BotPost:
    id: str
    content: str
    media_urls: Optional[List[str]]
    campaign: str
    channels: List[str]
    status: str  # 'draft', 'scheduled', 'published', 'failed'
    scheduled_time: Optional[str]
    published_time: Optional[str]
    created_at: str
    updated_at: str
```

## Обработка ошибок

### Режимы работы

1. **Полная интеграция** - когда бот доступен
2. **Тестовый режим** - когда бот недоступен

### Автоматическое переключение

Система автоматически определяет доступность бота и переключается между режимами:

```python
try:
    from telegram_autopost_bot.bot_integration import bot_integration
    BOT_INTEGRATION_AVAILABLE = True
except ImportError:
    BOT_INTEGRATION_AVAILABLE = False
```

### Логирование ошибок

Все ошибки логируются и отображаются в API ответах:

```json
{
    "success": false,
    "error": "Описание ошибки"
}
```

## Расширение функциональности

### Добавление новых кампаний

1. Обновите `config.py`:
```python
NEW_CAMPAIGN_CHANNELS = {
    'new_channel': {
        'chat_id': '-1001234567890',
        'name': 'New Channel',
        'active': True,
        'campaign': 'new_campaign'
    }
}
```

2. Добавьте расписание в `POSTING_SCHEDULE`:
```python
POSTING_SCHEDULE['new_campaign'] = {
    'monday': ['09:00', '18:00'],
    # ... остальные дни
}
```

### Добавление новых типов контента

1. Обновите `POST_TEMPLATES`:
```python
POST_TEMPLATES['new_campaign'] = {
    'new_type': """
    Новый шаблон контента
    {content}
    """,
}
```

2. Расширьте генератор контента в `bot_integration.py`

## Мониторинг и отладка

### Проверка статуса системы

```bash
curl http://localhost:5000/api/universal-bot/system-status
```

### Просмотр логов

```bash
# Логи API сервера
tail -f logs/api.log

# Логи бота
tail -f telegram_autopost_bot/logs/bot.log
```

### Тестирование интеграции

```bash
# Тест API
python -m pytest tests/test_integration.py

# Тест бота
cd telegram_autopost_bot
python -m pytest tests/test_bot.py
```

## Безопасность

### Аутентификация

- Все API эндпоинты защищены аутентификацией
- Используется сессионная аутентификация
- Проверка прав доступа к функциям бота

### Валидация данных

- Проверка входных данных
- Санитизация контента
- Защита от SQL-инъекций

### Ограничения доступа

- Только администратор может управлять ботом
- Проверка ADMIN_ID для критических операций

## Производительность

### Оптимизации

1. **Кэширование** - кэширование часто запрашиваемых данных
2. **Асинхронность** - неблокирующие операции
3. **Пакетная обработка** - группировка операций с базой данных

### Мониторинг

- Отслеживание времени ответа API
- Мониторинг использования памяти
- Логирование производительности

## Поддержка

### Частые проблемы

1. **Бот не запускается**
   - Проверьте токен в .env
   - Убедитесь в правильности ADMIN_ID

2. **API не отвечает**
   - Проверьте порт 5000
   - Убедитесь в запуске Flask сервера

3. **Ошибки интеграции**
   - Проверьте пути к модулям
   - Убедитесь в наличии всех файлов

### Получение помощи

1. Проверьте логи системы
2. Убедитесь в правильности конфигурации
3. Проверьте зависимости
4. Обратитесь к документации

## Дальнейшее развитие

### Планируемые улучшения

1. **Веб-хуки** - уведомления о событиях бота
2. **API ключи** - более гибкая аутентификация
3. **Многопользовательский режим** - поддержка нескольких администраторов
4. **Расширенная аналитика** - детальная статистика
5. **Интеграции** - подключение внешних сервисов

### Архитектурные улучшения

1. **Микросервисы** - разделение на отдельные сервисы
2. **Docker** - контейнеризация
3. **База данных** - переход на PostgreSQL
4. **Кэширование** - Redis для кэша
5. **Очереди** - Celery для фоновых задач 