from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import os
from config import DATABASE_PATH, SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
from datetime import datetime, timedelta
from functools import wraps

# Создаем приложение Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Разрешаем CORS для всех API эндпоинтов

# Устанавливаем секретный ключ для сессий
app.config['SECRET_KEY'] = SECRET_KEY

# Путь к базам данных
POSTS_DB_PATH = 'data/posts.db'
TELEGRAM_DB_PATH = DATABASE_PATH

def get_db_connection(db_path):
    """Создает соединение с базой данных."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- Декоратор для проверки аутентификации ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    """Инициализирует базу данных, создавая необходимые таблицы, если они не существуют."""
    # Убедимся, что директория 'data' существует
    data_dir = os.path.dirname(TELEGRAM_DB_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    conn_tg = get_db_connection(TELEGRAM_DB_PATH)
    # Создаем таблицу каналов, если ее нет
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id TEXT NOT NULL UNIQUE
        );
    ''')
    
    # Создаем таблицу курсов для новой функциональности
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            start_date TEXT,
            status TEXT NOT NULL DEFAULT 'draft' 
        );
    ''')

    # Создаем таблицу транзакций для финансового модуля
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, -- 'income' or 'expense'
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            category TEXT,
            course_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
    ''')

    # Создаем таблицу для управления командой
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE,
            status TEXT NOT NULL DEFAULT 'active' -- 'active', 'inactive'
        );
    ''')

    # Создаем таблицы для модуля рекламных кампаний
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT, -- e.g., 'Telegram Ads', 'Google Ads'
            budget REAL,
            start_date TEXT,
            end_date TEXT,
            status TEXT NOT NULL DEFAULT 'active' -- 'active', 'paused', 'finished'
        );
    ''')
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS campaign_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            impressions INTEGER,
            clicks INTEGER,
            cost REAL,
            conversions INTEGER,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        );
    ''')

    # Создаем таблицы для аналитики студентов
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            registration_date TEXT NOT NULL
        );
    ''')
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active', -- 'active', 'completed', 'dropped'
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
    ''')

    # Создаем таблицы для партнерской программы
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            promo_code TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'active' -- 'active', 'inactive'
        );
    ''')
    conn_tg.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            referral_date TEXT NOT NULL,
            commission_amount REAL,
            FOREIGN KEY (partner_id) REFERENCES partners(id),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
    ''')
    
    conn_tg.commit()
    conn_tg.close()

# --- Маршруты аутентификации ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('owner_dashboard'))
        else:
            flash('Неверные учетные данные. Попробуйте еще раз.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

# --- API эндпоинты ---
@app.route('/')
@login_required
def owner_dashboard():
    return render_template('new_dashboard.html')

@app.route('/api/owner/summary', methods=['GET'])
@login_required
def get_owner_summary():
    """
    Эндпоинт для главной панели владельца.
    Собирает агрегированные данные со всей системы.
    """
    try:
        # --- Финансовые показатели (пока что статичные) ---
        financials = {
            'totalRevenue': 2847500,
            'profitMargin': 68,
            'monthly': {
                'grossRevenue': 485700,
                'expenses': 156200,
                'netProfit': 329500
            }
        }

        # --- Данные по студентам (статичные) ---
        students = {
            'total': 1247,
            'satisfaction': 94,
            'completionRate': 87,
            'ltv': 38450,
            'cac': 4200
        }

        # --- Данные по курсам (статичные) ---
        courses = {
            'active': 12,
            'topByProfit': [
                {'name': 'UX/UI Pro', 'share': 35},
                {'name': 'Mobile Design', 'share': 25},
                {'name': 'Design Systems', 'share': 20},
                {'name': 'UX Research', 'share': 12},
                {'name': 'Figma Mastery', 'share': 8}
            ]
        }
        
        # --- Динамика доходов для графика (статичные) ---
        revenue_dynamics = {
            'labels': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
            'revenue': [320000, 385000, 420000, 465000, 485000, 510000],
            'profit': [190000, 245000, 275000, 310000, 329500, 350000]
        }

        # --- Собираем все в один ответ ---
        summary = {
            'financials': financials,
            'students': students,
            'courses': courses,
            'charts': {
                'revenue': revenue_dynamics
            }
        }

        return jsonify(summary)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/content/summary', methods=['GET'])
def get_content_summary():
    """
    Эндпоинт для дашборда генерации контента.
    Возвращает статистику по постам и доступные опции для генерации.
    """
    try:
        # --- Статистика по постам ---
        conn_posts = get_db_connection(POSTS_DB_PATH)
        total_posts = conn_posts.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        # TODO: Добавить подсчет постов "в очереди" и "сгенерировано сегодня"
        conn_posts.close()

        stats = {
            'postsInQueue': 15, # Заглушка
            'generatedToday': 7, # Заглушка
            'totalInDb': total_posts
        }

        # --- Опции для генерации (пока статичные) ---
        options = {
            'templates': ['Universal Content Template', 'News Post', 'Promotional Post'],
            'themes': ['UX/UI Design Basics', 'Figma Tricks', 'Career in IT', 'Mobile Design'],
            'audiences': ['Juniors', 'Designers', 'Freelancers', 'Students']
        }

        summary = {
            'stats': stats,
            'options': options
        }

        return jsonify(summary)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/scheduled_posts', methods=['GET'])
def get_scheduled_posts():
    """
    Возвращает запланированные посты для календаря.
    Принимает 'year' и 'month' как параметры запроса.
    """
    year = request.args.get('year')
    month = request.args.get('month')

    if not year or not month:
        return jsonify({'error': 'Year and month parameters are required'}), 400

    try:
        # Формируем строку для поиска по месяцу, например, '2024-07%'
        month_str = f"{year}-{int(month):02d}-"
        
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        # Считаем количество постов на каждый день указанного месяца
        query = """
        SELECT 
            strftime('%Y-%m-%d', scheduled_date) as post_day, 
            COUNT(id) as post_count
        FROM posts
        WHERE scheduled_date LIKE ?
        GROUP BY post_day
        """
        posts_by_day = conn_tg.execute(query, (month_str + '%',)).fetchall()
        conn_tg.close()

        # Преобразуем результат в удобный для фронтенда формат
        # {'2024-07-15': {'post_count': 2}, ...}
        scheduled_data = {row['post_day']: {'post_count': row['post_count']} for row in posts_by_day}

        return jsonify(scheduled_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/main_summary', methods=['GET'])
def get_telegram_main_summary():
    """
    Возвращает сводную информацию для главного дашборда Telegram-бота.
    """
    try:
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        
        total_posts = conn_tg.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        published_posts = conn_tg.execute('SELECT COUNT(id) FROM posts WHERE published = 1').fetchone()[0]
        pending_posts = total_posts - published_posts
        
        # Получаем реальное количество каналов из новой таблицы
        total_groups = conn_tg.execute('SELECT COUNT(id) FROM channels').fetchone()[0]

        # Запрос последних 5 активностей (пока имитируем)
        # В реальной системе здесь должен быть запрос к таблице логов или событий
        recent_activities = [
            {'type': 'success', 'text': 'Пост в "UX/UI Academy" успешно опубликован.', 'time': '2 минуты назад'},
            {'type': 'info', 'text': 'Запланирован новый пост в "Design News".', 'time': '1 час назад'},
            {'type': 'error', 'text': 'Ошибка публикации в "Test Channel": неверный chat_id.', 'time': '3 часа назад'},
            {'type': 'success', 'text': 'Пост в "UX/UI Academy" успешно опубликован.', 'time': '5 часов назад'},
            {'type': 'info', 'text': 'Бот успешно перезапущен.', 'time': '8 часов назад'}
        ]

        # Данные для графика (пока статичные)
        publication_chart_data = {
            'labels': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            'published': [5, 8, 12, 7, 10, 15, 9],
            'scheduled': [3, 4, 2, 5, 6, 3, 7]
        }
        
        conn_tg.close()

        summary = {
            'bot_status': {'online': True, 'message': 'Бот в сети'},
            'stats': {
                'total_posts': total_posts,
                'total_groups': total_groups,
                'published_posts': published_posts,
                'pending_posts': pending_posts
            },
            'recent_activities': recent_activities,
            'charts': {
                'publications': publication_chart_data
            }
        }
        return jsonify(summary)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/groups', methods=['GET'])
def get_groups():
    """Возвращает список всех каналов."""
    try:
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        channels = conn_tg.execute('SELECT id, name, chat_id FROM channels ORDER BY name').fetchall()
        conn_tg.close()
        return jsonify([dict(row) for row in channels])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/groups', methods=['POST'])
def add_group():
    """Добавляет новый канал."""
    data = request.get_json()
    name = data.get('name')
    chat_id = data.get('chat_id')

    if not name or not chat_id:
        return jsonify({'error': 'Name and chat_id are required'}), 400

    try:
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        conn_tg.execute('INSERT INTO channels (name, chat_id) VALUES (?, ?)', (name, chat_id))
        conn_tg.commit()
        conn_tg.close()
        return jsonify({'message': 'Channel added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Channel with this chat_id already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Удаляет канал по ID."""
    try:
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        conn_tg.execute('DELETE FROM channels WHERE id = ?', (group_id,))
        conn_tg.commit()
        conn_tg.close()
        return jsonify({'message': 'Channel deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/telegram/stats', methods=['GET'])
def get_telegram_stats():
    """
    Возвращает детальную статистику для страницы аналитики.
    """
    try:
        conn_tg = get_db_connection(TELEGRAM_DB_PATH)
        
        # 1. Общие метрики
        total_posts = conn_tg.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        published_posts = conn_tg.execute('SELECT COUNT(id) FROM posts WHERE published = 1').fetchone()[0]
        success_rate = (published_posts / total_posts * 100) if total_posts > 0 else 0
        
        # 2. Посты за последние 30 дней для линейного графика
        posts_last_30_days = conn_tg.execute("""
            SELECT strftime('%Y-%m-%d', scheduled_date) as day, COUNT(id) as count
            FROM posts
            WHERE scheduled_date >= date('now', '-30 days') AND published = 1
            GROUP BY day
            ORDER BY day
        """).fetchall()

        # 3. Распределение постов по каналам для круговой диаграммы
        posts_by_channel = conn_tg.execute("""
            SELECT c.name, COUNT(p.id) as count
            FROM posts p
            JOIN channels c ON p.channel_id = c.chat_id
            WHERE p.published = 1
            GROUP BY c.name
            ORDER BY count DESC
        """).fetchall()
        
        # 4. Самый активный канал
        most_active_channel = posts_by_channel[0]['name'] if posts_by_channel else 'N/A'
        
        # 5. Среднее число постов в день
        total_days = conn_tg.execute("SELECT julianday(MAX(scheduled_date)) - julianday(MIN(scheduled_date)) FROM posts WHERE published = 1").fetchone()[0]
        avg_posts_per_day = (published_posts / total_days) if total_days and total_days > 0 else 0

        # 6. Детальная статистика по каналам для таблицы
        channels_details = conn_tg.execute("""
            SELECT 
                c.id, c.name, c.chat_id, 
                COUNT(p.id) as total_posts,
                SUM(CASE WHEN p.published = 1 THEN 1 ELSE 0 END) as published_posts
            FROM channels c
            LEFT JOIN posts p ON c.chat_id = p.channel_id
            GROUP BY c.id, c.name, c.chat_id
            ORDER BY total_posts DESC
        """).fetchall()

        conn_tg.close()

        stats = {
            'overview': {
                'total_published': published_posts,
                'avg_per_day': round(avg_posts_per_day, 1),
                'most_active_channel': most_active_channel,
                'success_rate': round(success_rate, 2)
            },
            'charts': {
                'publications_trend': {
                    'labels': [row['day'] for row in posts_last_30_days],
                    'data': [row['count'] for row in posts_last_30_days]
                },
                'posts_by_channel': {
                    'labels': [row['name'] for row in posts_by_channel],
                    'data': [row['count'] for row in posts_by_channel]
                }
            },
            'channels_table': [dict(row) for row in channels_details]
        }
        
        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для курсов ---

@app.route('/api/courses', methods=['POST'])
def add_course():
    """Добавляет новый курс."""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        start_date = data.get('start_date')

        if not name or price is None:
            return jsonify({'error': 'Название и цена являются обязательными полями'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO courses (name, description, price, start_date) VALUES (?, ?, ?, ?)',
            (name, description, price, start_date)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Курс успешно добавлен'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Возвращает список всех курсов."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        courses = conn.execute('SELECT * FROM courses ORDER BY id DESC').fetchall()
        conn.close()
        return jsonify([dict(row) for row in courses])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Обновляет существующий курс."""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        start_date = data.get('start_date')
        status = data.get('status')

        if not name or price is None or status is None:
            return jsonify({'error': 'Название, цена и статус являются обязательными полями'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'UPDATE courses SET name = ?, description = ?, price = ?, start_date = ?, status = ? WHERE id = ?',
            (name, description, price, start_date, status, course_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Курс успешно обновлен'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Удаляет курс."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Курс успешно удален'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для Транзакций ---

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    """Добавляет новую транзакцию."""
    try:
        data = request.get_json()
        # Простая валидация
        if not all(k in data for k in ['type', 'amount', 'description', 'date', 'category']):
            return jsonify({'error': 'Не все поля были предоставлены'}), 400
        
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO transactions (type, amount, description, date, category, course_id) VALUES (?, ?, ?, ?, ?, ?)',
            (data['type'], data['amount'], data['description'], data['date'], data['category'], data.get('course_id'))
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Транзакция успешно добавлена'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Возвращает список транзакций с фильтрацией."""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        conn = get_db_connection(TELEGRAM_DB_PATH)
        
        query = 'SELECT t.*, c.name as course_name FROM transactions t LEFT JOIN courses c ON t.course_id = c.id'
        params = []
        
        if start_date and end_date:
            query += ' WHERE t.date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        
        query += ' ORDER BY t.date DESC'
        
        transactions = conn.execute(query, params).fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in transactions])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для Команды ---

@app.route('/api/team', methods=['POST'])
def add_team_member():
    """Добавляет нового члена команды."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('role'):
            return jsonify({'error': 'Имя и роль обязательны'}), 400
        
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO team_members (name, role, email) VALUES (?, ?, ?)',
            (data['name'], data['role'], data.get('email'))
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Сотрудник добавлен'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Сотрудник с таким email уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team', methods=['GET'])
def get_team_members():
    """Возвращает список всех членов команды."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        members = conn.execute('SELECT * FROM team_members ORDER BY name').fetchall()
        conn.close()
        return jsonify([dict(row) for row in members])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team/<int:member_id>', methods=['PUT'])
def update_team_member(member_id):
    """Обновляет данные члена команды."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('role') or not data.get('status'):
            return jsonify({'error': 'Имя, роль и статус обязательны'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'UPDATE team_members SET name = ?, role = ?, email = ?, status = ? WHERE id = ?',
            (data['name'], data['role'], data.get('email'), data['status'], member_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные сотрудника обновлены'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Сотрудник с таким email уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team/<int:member_id>', methods=['DELETE'])
def delete_team_member(member_id):
    """Удаляет члена команды."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute('DELETE FROM team_members WHERE id = ?', (member_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Сотрудник удален'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для Рекламных кампаний ---

@app.route('/api/campaigns', methods=['POST'])
def add_campaign():
    """Добавляет новую рекламную кампанию."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('budget'):
            return jsonify({'error': 'Название и бюджет обязательны'}), 400
        
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO campaigns (name, source, budget, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
            (data['name'], data.get('source'), data['budget'], data.get('start_date'), data.get('end_date'))
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Кампания добавлена'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    """Возвращает список всех кампаний с агрегированной статистикой."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        # Этот запрос объединяет кампании с их суммарной статистикой
        query = """
            SELECT 
                c.*,
                SUM(cs.cost) as total_cost,
                SUM(cs.clicks) as total_clicks,
                SUM(cs.conversions) as total_conversions
            FROM campaigns c
            LEFT JOIN campaign_stats cs ON c.id = cs.campaign_id
            GROUP BY c.id
            ORDER BY c.start_date DESC
        """
        campaigns = conn.execute(query).fetchall()
        conn.close()
        return jsonify([dict(row) for row in campaigns])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Обновляет данные рекламной кампании."""
    try:
        data = request.get_json()
        if not all(k in data for k in ['name', 'budget', 'status']):
            return jsonify({'error': 'Название, бюджет и статус обязательны'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'UPDATE campaigns SET name=?, source=?, budget=?, start_date=?, end_date=?, status=? WHERE id=?',
            (data['name'], data.get('source'), data['budget'], data.get('start_date'), data.get('end_date'), data['status'], campaign_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные кампании обновлены'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Удаляет кампанию и связанную с ней статистику."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        # Сначала удаляем статистику, чтобы не нарушить foreign key constraint
        conn.execute('DELETE FROM campaign_stats WHERE campaign_id = ?', (campaign_id,))
        # Затем удаляем саму кампанию
        conn.execute('DELETE FROM campaigns WHERE id = ?', (campaign_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Кампания и ее статистика удалены'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для Студентов ---

@app.route('/api/students', methods=['POST'])
def add_student():
    """Добавляет нового студента."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('email') or not data.get('registration_date'):
            return jsonify({'error': 'Имя, email и дата регистрации обязательны'}), 400
        
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO students (name, email, registration_date) VALUES (?, ?, ?)',
            (data['name'], data['email'], data['registration_date'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Студент добавлен'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Студент с таким email уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """Возвращает список всех студентов."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        students = conn.execute('SELECT * FROM students ORDER BY registration_date DESC').fetchall()
        conn.close()
        return jsonify([dict(row) for row in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Обновляет данные студента."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Имя и email обязательны'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'UPDATE students SET name=?, email=? WHERE id=?',
            (data['name'], data['email'], student_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные студента обновлены'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Студент с таким email уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Удаляет студента и все его записи на курсы."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        # Сначала удаляем записи на курсы
        conn.execute('DELETE FROM enrollments WHERE student_id = ?', (student_id,))
        # Затем самого студента
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Студент и все его данные удалены'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CRUD для Партнеров ---

@app.route('/api/partners', methods=['POST'])
def add_partner():
    """Добавляет нового партнера."""
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('promo_code'):
            return jsonify({'error': 'Имя и промокод обязательны'}), 400
        
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'INSERT INTO partners (name, email, promo_code) VALUES (?, ?, ?)',
            (data['name'], data.get('email'), data['promo_code'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Партнер добавлен'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Партнер с таким email или промокодом уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/partners', methods=['GET'])
def get_partners():
    """Возвращает список партнеров со статистикой по рефералам."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        query = """
            SELECT 
                p.*,
                COUNT(r.id) as referral_count
            FROM partners p
            LEFT JOIN referrals r ON p.id = r.partner_id
            GROUP BY p.id
            ORDER BY p.name
        """
        partners = conn.execute(query).fetchall()
        conn.close()
        return jsonify([dict(row) for row in partners])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/partners/<int:partner_id>', methods=['PUT'])
def update_partner(partner_id):
    """Обновляет данные партнера."""
    try:
        data = request.get_json()
        if not all(k in data for k in ['name', 'promo_code', 'status']):
            return jsonify({'error': 'Имя, промокод и статус обязательны'}), 400

        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute(
            'UPDATE partners SET name=?, email=?, promo_code=?, status=? WHERE id=?',
            (data['name'], data.get('email'), data['promo_code'], data['status'], partner_id)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные партнера обновлены'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Партнер с таким email или промокодом уже существует'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/partners/<int:partner_id>', methods=['DELETE'])
def delete_partner(partner_id):
    """Удаляет партнера и его рефералов."""
    try:
        conn = get_db_connection(TELEGRAM_DB_PATH)
        conn.execute('DELETE FROM referrals WHERE partner_id = ?', (partner_id,))
        conn.execute('DELETE FROM partners WHERE id = ?', (partner_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Партнер и его рефералы удалены'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Рендеринг страниц ---
@app.route('/manage-courses')
@login_required
def manage_courses_page():
    """Открывает страницу управления курсами."""
    return render_template('manage_courses.html')

@app.route('/financial-report')
@login_required
def financial_report_page():
    """Открывает страницу финансового отчета."""
    return render_template('financial_report.html')

@app.route('/manage-team')
@login_required
def manage_team_page():
    """Открывает страницу управления командой."""
    return render_template('manage_team.html')

@app.route('/manage-campaigns')
@login_required
def manage_campaigns_page():
    """Открывает страницу управления рекламными кампаниями."""
    return render_template('manage_campaigns.html')

@app.route('/student-analytics')
@login_required
def student_analytics_page():
    """Открывает страницу аналитики студентов."""
    return render_template('student_analytics.html')

@app.route('/partner-program')
@login_required
def partner_program_page():
    return render_template('partner_program.html')

@app.route('/telegram-bot')
@login_required
def telegram_bot_page():
    """Открывает страницу Telegram Bot дашборда."""
    return render_template('telegram_bot_main_dashboard.html')

@app.route('/content-generator')
@login_required
def content_generator_page():
    """Открывает страницу генератора контента."""
    return render_template('content_generator_dashboard.html')

if __name__ == '__main__':
    init_db() # Вызываем инициализацию БД при старте
    # Запускаем сервер на порту 5001, чтобы не конфликтовать с другими сервисами
    app.run(debug=True, port=5001) 