# 🔧 Настройка .env файла для "Digitalizacija Biznesa"

## 📋 Пошаговая инструкция

### Шаг 1: Создание .env файла

1. Откройте папку `telegram_autopost_bot/`
2. Создайте новый файл с именем `.env` (без расширения)
3. Откройте файл в любом текстовом редакторе

### Шаг 2: Добавление содержимого

Скопируйте и вставьте следующий код в файл `.env`:

```env
# ========================================
# НАСТРОЙКИ БОТА TELEGRAM
# ========================================

# Токен вашего бота (получите у @BotFather)
BOT_TOKEN=your_bot_token_here

# ID администратора (ваш Telegram ID)
ADMIN_ID=your_telegram_id_here

# ========================================
# ID КАНАЛОВ И ГРУПП "DIGITALIZACIJA BIZNESA"
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
LEAD_BOT_TOKEN=your_bot_token_here

# Настройки базы данных
DATABASE_PATH=data/

# Настройки отчетов
REPORTS_PATH=reports/

# Режим отладки (true/false)
DEBUG_MODE=false
```

---

## 🎯 Получение необходимых данных

### 1. Получение токена бота

#### Пошаговая инструкция:

1. **Откройте Telegram**
2. **Найдите @BotFather**
3. **Отправьте команду:** `/newbot`
4. **Введите имя бота:** `Digitalizacija Biznesa Bot`
5. **Введите username:** `digitalizacija_biznesa_bot` (должен заканчиваться на "bot")
6. **Получите токен** вида: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### Пример диалога:
```
Вы: /newbot
BotFather: Alright, a new bot. How are we going to call it? Please choose a name for your bot.
Вы: Digitalizacija Biznesa Bot
BotFather: Good. Now let's choose a username for your bot. It must end in `bot`. Like this: TetrisBot or tetris_bot.
Вы: digitalizacija_biznesa_bot
BotFather: Done! Congratulations on your new bot. You will find it at t.me/digitalizacija_biznesa_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

### 2. Получение вашего Telegram ID

#### Пошаговая инструкция:

1. **Откройте Telegram**
2. **Найдите @userinfobot**
3. **Отправьте любое сообщение** (например: "Привет")
4. **Получите ваш ID** (например: `987654321`)

#### Пример ответа:
```
@userinfobot: 
👤 User Info:
🆔 ID: 987654321
👤 Name: Ваше Имя
📝 Username: @your_username
📱 Phone: +7 xxx xxx xx xx
```

### 3. Создание каналов и групп

#### Создание каналов:

1. **Откройте Telegram**
2. **Нажмите на меню** (три полоски)
3. **Выберите "Создать канал"**
4. **Введите название канала:**
   - `Digitalizacija Biznesa` (основной)
   - `Бизнес Автоматизация` (кейсы)
   - `Стартап Digital` (стартапы)
5. **Добавьте описание**
6. **Сделайте канал публичным** (если нужно)

#### Создание групп:

1. **Откройте Telegram**
2. **Нажмите на меню** (три полоски)
3. **Выберите "Создать группу"**
4. **Введите название группы:**
   - `Digitalizacija Community` (сообщество)
   - `Бизнес Консультации` (консультации)
   - `Автоматизация Советы` (советы)
5. **Добавьте описание**

### 4. Добавление бота как администратора

#### Для каждого канала/группы:

1. **Откройте канал/группу**
2. **Нажмите на название** (вверху)
3. **Выберите "Администраторы"**
4. **Нажмите "Добавить администратора"**
5. **Найдите вашего бота** по username
6. **Назначьте права:**
   - ✅ Отправка сообщений
   - ✅ Редактирование сообщений
   - ✅ Удаление сообщений
   - ✅ Закрепление сообщений
   - ✅ Приглашение пользователей

### 5. Получение ID каналов и групп

#### Метод 1: Через getUpdates

1. **Отправьте команду `/start`** в каждый канал/группу
2. **Перейдите по ссылке** (замените `<BOT_TOKEN>` на ваш токен):
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
3. **Найдите в ответе** строки вида:
   ```json
   "chat":{"id":-1001234567890,"title":"Digitalizacija Biznesa","type":"channel"}
   ```
4. **Скопируйте ID** (например: `-1001234567890`)

#### Метод 2: Через бота @getidsbot

1. **Найдите @getidsbot** в Telegram
2. **Добавьте его в канал/группу**
3. **Отправьте команду** `/getgroupid`
4. **Получите ID** канала/группы

---

## 📝 Заполнение .env файла

### Пример заполненного файла:

```env
# ========================================
# НАСТРОЙКИ БОТА TELEGRAM
# ========================================

BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=987654321

# ========================================
# ID КАНАЛОВ И ГРУПП "DIGITALIZACIJA BIZNESA"
# ========================================

DIGITALIZACIJA_MAIN_CHANNEL_ID=-1001234567890
BIZNES_AUTOMATION_CHANNEL_ID=-1001234567891
STARTUP_DIGITAL_CHANNEL_ID=-1001234567892
DIGITALIZACIJA_COMMUNITY_ID=-1001234567893
BIZNES_CONSULTING_ID=-1001234567894
AUTOMATION_TIPS_ID=-1001234567895

# ========================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ========================================

LEAD_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DATABASE_PATH=data/
REPORTS_PATH=reports/
DEBUG_MODE=false
```

---

## ✅ Проверка настроек

### Запуск проверки:

```bash
cd telegram_autopost_bot
python check_env.py
```

### Ожидаемый результат:

```
🔍 ПРОВЕРКА НАСТРОЕК .ENV ФАЙЛА
==================================================

📋 ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ:
✅ BOT_TOKEN: ********** (настроено)
✅ ADMIN_ID: ********** (настроено)

📺 ID КАНАЛОВ И ГРУПП:
✅ DIGITALIZACIJA_MAIN_CHANNEL_ID: -1001234567890
✅ BIZNES_AUTOMATION_CHANNEL_ID: -1001234567891
✅ STARTUP_DIGITAL_CHANNEL_ID: -1001234567892
✅ DIGITALIZACIJA_COMMUNITY_ID: -1001234567893
✅ BIZNES_CONSULTING_ID: -1001234567894
✅ AUTOMATION_TIPS_ID: -1001234567895

⚙️ ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ:
✅ LEAD_BOT_TOKEN: ********** (настроено)
✅ DATABASE_PATH: data/
✅ REPORTS_PATH: reports/
✅ DEBUG_MODE: false

📊 ИТОГОВАЯ ОЦЕНКА:
🎉 ВСЕ НАСТРОЙКИ ЗАПОЛНЕНЫ!
✅ Система готова к запуску
```

---

## 🚨 Частые проблемы

### Проблема: "BOT_TOKEN не настроен"

**Решение:**
1. Проверьте, что файл называется именно `.env` (не `.env.txt`)
2. Убедитесь, что токен скопирован полностью
3. Проверьте, что нет лишних пробелов

### Проблема: "ID канала не найден"

**Решение:**
1. Убедитесь, что бот добавлен как администратор
2. Отправьте `/start` в канал
3. Проверьте ссылку getUpdates еще раз

### Проблема: "Бот не может отправлять сообщения"

**Решение:**
1. Проверьте права администратора
2. Убедитесь, что бот активен
3. Проверьте токен на правильность

---

## 🎯 Следующие шаги

После успешной настройки .env файла:

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   pip install pandas matplotlib seaborn schedule
   ```

2. **Запустите систему:**
   ```bash
   python start_complete_system.py
   ```

3. **Проверьте работу:**
   - Приветственные посты отправлены
   - Планировщик работает
   - Бот лидогенерации отвечает

---

## 📞 Поддержка

Если возникли проблемы:

1. **Запустите проверку:** `python check_env.py`
2. **Проверьте логи** в консоли
3. **Убедитесь в правах** бота в каналах
4. **Проверьте токен** на правильность

**Система готова к работе! 🚀** 