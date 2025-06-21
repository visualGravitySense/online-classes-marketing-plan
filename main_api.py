from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

# Создаем приложение Flask
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех маршрутов

# Путь к базам данных
POSTS_DB_PATH = 'data/posts.db'
TELEGRAM_DB_PATH = 'telegram_autopost_bot/data/posts.db'

def get_db_connection(db_path):
    """Создает соединение с базой данных."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует базу данных, создает таблицы, если их нет."""
    conn_tg = get_db_connection(TELEGRAM_DB_PATH)
    cursor = conn_tg.cursor()
    
    # Создаем таблицу каналов, если она не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        chat_id TEXT NOT NULL UNIQUE
    )
    """)
    
    # Можно добавить другие таблицы здесь в будущем
    
    conn_tg.commit()
    conn_tg.close()

@app.route('/')
def index():
    return "<h1>API Gateway for UX/UI Academy is running!</h1>"

@app.route('/api/owner/summary', methods=['GET'])
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

if __name__ == '__main__':
    init_db() # Вызываем инициализацию БД при старте
    # Запускаем сервер на порту 5001, чтобы не конфликтовать с другими сервисами
    app.run(debug=True, port=5001) 