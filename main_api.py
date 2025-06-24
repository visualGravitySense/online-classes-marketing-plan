from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import os
from config import DATABASE_PATH, SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
from datetime import datetime, timedelta
from functools import wraps
import time
import sys
from dataclasses import asdict

# Создаем приложение Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Разрешаем CORS для всех API эндпоинтов

# Устанавливаем секретный ключ для сессий
app.config['SECRET_KEY'] = SECRET_KEY

# Путь к базам данных
POSTS_DB_PATH = 'data/posts.db'
TELEGRAM_DB_PATH = DATABASE_PATH

# ===== ИМПОРТ ИНТЕГРАЦИИ С БОТОМ =====
# Добавляем путь к папке с ботом
bot_path = os.path.join(os.path.dirname(__file__), 'telegram_autopost_bot')
sys.path.append(bot_path)

try:
    from bot_integration import bot_integration
    BOT_INTEGRATION_AVAILABLE = True
    print("✅ Интеграция с ботом подключена")
except ImportError as e:
    print(f"⚠️  Предупреждение: Не удалось импортировать интеграцию с ботом: {e}")
    print("   Система будет работать в тестовом режиме")
    BOT_INTEGRATION_AVAILABLE = False

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

# --- Основные маршруты ---
@app.route('/')
def index():
    return redirect(url_for('owner_dashboard'))

@app.route('/owner-dashboard')
@login_required
def owner_dashboard():
    return render_template('owner_dashboard.html')

# ===== API ЭНДПОИНТЫ ДЛЯ УНИВЕРСАЛЬНОГО БОТА =====

@app.route('/api/universal-bot/dashboard', methods=['GET'])
@login_required
def get_universal_bot_dashboard():
    """Получение данных дашборда универсального бота"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальные данные от бота
            dashboard_data = bot_integration.get_dashboard_data()
        else:
            # Возвращаем тестовые данные если интеграция недоступна
            dashboard_data = {
                'campaigns': {
                    'total': 3,
                    'active': 2,
                    'inactive': 1
                },
                'posts': {
                    'total': 156,
                    'published': 144,
                    'scheduled': 12,
                    'failed': 0
                },
                'channels': {
                    'total': 8,
                    'active': 7,
                    'inactive': 1
                },
                'engagement': {
                    'average_engagement_rate': 4.2,
                    'total_views': 15420,
                    'total_likes': 648,
                    'total_shares': 234
                }
            }
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/campaigns', methods=['GET'])
@login_required
def get_universal_bot_campaigns():
    """Получение списка кампаний универсального бота"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальные данные от бота
            campaigns = bot_integration.get_campaigns_data()
            # Конвертируем dataclass в dict
            campaigns_data = [asdict(campaign) for campaign in campaigns]
        else:
            # Возвращаем тестовые данные
            campaigns_data = [
                {
                    'id': 'uxui-campaign',
                    'name': 'UX/UI Дизайн',
                    'description': 'Кампания для продвижения курсов по UX/UI дизайну',
                    'status': 'active',
                    'channels': [
                        {'id': 'channel1', 'name': 'UX/UI Designers', 'chat_id': '-1001234567890'},
                        {'id': 'channel2', 'name': 'Design Community', 'chat_id': '-1001234567891'}
                    ],
                    'posts_count': 89,
                    'scheduled_posts': 5,
                    'created_at': '2024-01-15T10:00:00Z',
                    'updated_at': '2024-01-20T15:30:00Z'
                },
                {
                    'id': 'digitalizacija-campaign',
                    'name': 'Цифровизация бизнеса',
                    'description': 'Кампания для продвижения услуг цифровизации',
                    'status': 'active',
                    'channels': [
                        {'id': 'channel3', 'name': 'Business Digital', 'chat_id': '-1001234567892'},
                        {'id': 'channel4', 'name': 'Startup Hub', 'chat_id': '-1001234567893'}
                    ],
                    'posts_count': 67,
                    'scheduled_posts': 7,
                    'created_at': '2024-01-10T09:00:00Z',
                    'updated_at': '2024-01-19T14:20:00Z'
                }
            ]
        
        return jsonify({
            'success': True,
            'data': campaigns_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/campaigns', methods=['POST'])
@login_required
def create_universal_bot_campaign():
    """Создание новой кампании"""
    try:
    data = request.get_json()
        
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальную логику создания кампании
            campaign = bot_integration.create_campaign(
                name=data.get('name'),
                description=data.get('description', ''),
                channels=data.get('channels', [])
            )
            campaign_data = asdict(campaign)
        else:
            # Тестовая логика
            campaign_id = f"campaign-{int(time.time())}"
            campaign_data = {
                'id': campaign_id,
                'name': data.get('name'),
                'description': data.get('description'),
                'status': 'inactive',
                'channels': [],
                'posts_count': 0,
                'scheduled_posts': 0,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        
        return jsonify({
            'success': True,
            'data': campaign_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/campaigns/<campaign_id>/start', methods=['POST'])
@login_required
def start_universal_bot_campaign(campaign_id):
    """Запуск кампании"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            success = bot_integration.start_campaign(campaign_id)
        else:
            success = True  # Тестовая логика
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Кампания {campaign_id} запущена'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Не удалось запустить кампанию {campaign_id}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/campaigns/<campaign_id>/pause', methods=['POST'])
@login_required
def pause_universal_bot_campaign(campaign_id):
    """Приостановка кампании"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            success = bot_integration.pause_campaign(campaign_id)
        else:
            success = True  # Тестовая логика
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Кампания {campaign_id} приостановлена'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Не удалось приостановить кампанию {campaign_id}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/campaigns/<campaign_id>', methods=['DELETE'])
@login_required
def delete_universal_bot_campaign(campaign_id):
    """Удаление кампании"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            success = bot_integration.delete_campaign(campaign_id)
        else:
            success = True  # Тестовая логика
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Кампания {campaign_id} удалена'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Не удалось удалить кампанию {campaign_id}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/channels', methods=['GET'])
@login_required
def get_universal_bot_channels():
    """Получение списка каналов"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальные данные от бота
            channels = bot_integration.get_channels_data()
            channels_data = [asdict(channel) for channel in channels]
        else:
            # Возвращаем тестовые данные
            channels_data = [
                {'id': 'channel1', 'name': 'UX/UI Designers', 'chat_id': '-1001234567890', 'campaign': 'uxui-campaign', 'status': 'active'},
                {'id': 'channel2', 'name': 'Design Community', 'chat_id': '-1001234567891', 'campaign': 'uxui-campaign', 'status': 'active'},
                {'id': 'channel3', 'name': 'Business Digital', 'chat_id': '-1001234567892', 'campaign': 'digitalizacija-campaign', 'status': 'active'},
                {'id': 'channel4', 'name': 'Startup Hub', 'chat_id': '-1001234567893', 'campaign': 'digitalizacija-campaign', 'status': 'active'}
            ]
        
        return jsonify({
            'success': True,
            'data': channels_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/posts', methods=['GET'])
@login_required
def get_universal_bot_posts():
    """Получение списка постов"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальные данные от бота
            posts = bot_integration.get_posts_data()
            posts_data = [asdict(post) for post in posts]
        else:
            # Возвращаем тестовые данные
            posts_data = [
                {
                    'id': 'post1',
                    'content': '🎨 Хотите стать UX/UI дизайнером? Наш курс поможет вам освоить все необходимые навыки! #UX #UI #дизайн',
                    'campaign': 'uxui-campaign',
                    'channels': ['channel1', 'channel2'],
                    'status': 'published',
                    'published_time': '2024-01-20T10:00:00Z',
                    'created_at': '2024-01-19T15:00:00Z',
                    'updated_at': '2024-01-20T10:00:00Z'
                },
                {
                    'id': 'post2',
                    'content': '🚀 Цифровизация бизнеса - ключ к успеху в современном мире. Узнайте, как автоматизировать ваши процессы! #цифровизация #бизнес',
                    'campaign': 'digitalizacija-campaign',
                    'channels': ['channel3', 'channel4'],
                    'status': 'scheduled',
                    'scheduled_time': '2024-01-21T14:00:00Z',
                    'created_at': '2024-01-20T12:00:00Z',
                    'updated_at': '2024-01-20T12:00:00Z'
                }
            ]
        
        return jsonify({
            'success': True,
            'data': posts_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/posts', methods=['POST'])
@login_required
def create_universal_bot_post():
    """Создание нового поста"""
    try:
        data = request.get_json()
        
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальную логику создания поста
            post = bot_integration.create_post(
                content=data.get('content'),
                campaign=data.get('campaign'),
                channels=data.get('channels', []),
                scheduled_time=data.get('scheduled_time')
            )
            post_data = asdict(post)
        else:
            # Тестовая логика
            post_id = f"post-{int(time.time())}"
            post_data = {
                'id': post_id,
                'content': data.get('content'),
                'campaign': data.get('campaign'),
                'channels': data.get('channels', []),
                'status': 'draft',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        
        return jsonify({
            'success': True,
            'data': post_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/posts/<post_id>', methods=['DELETE'])
@login_required
def delete_universal_bot_post(post_id):
    """Удаление поста"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            success = bot_integration.delete_post(post_id)
        else:
            success = True  # Тестовая логика
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Пост {post_id} удален'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Не удалось удалить пост {post_id}'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/generate-content', methods=['POST'])
@login_required
def generate_universal_bot_content():
    """Генерация контента"""
    try:
        data = request.get_json()
        
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальную логику генерации контента
            generated_content = bot_integration.generate_content(
                topic=data.get('topic', 'UX/UI дизайн'),
                campaign=data.get('campaign', 'default'),
                tone=data.get('tone', 'professional'),
                length=data.get('length', 'medium'),
                target_audience=data.get('target_audience', ''),
                platform=data.get('platform', 'telegram'),
                include_hashtags=data.get('include_hashtags', True),
                include_call_to_action=data.get('include_call_to_action', True)
            )
        else:
            # Тестовая логика генерации контента
            topic = data.get('topic', 'UX/UI дизайн')
            tone = data.get('tone', 'professional')
            platform = data.get('platform', 'telegram')
            
            content_templates = {
                'professional': f"🎯 {topic} - важная тема для современных специалистов. Изучайте, практикуйтесь и развивайтесь!",
                'casual': f"Привет! 👋 Сегодня поговорим о {topic}. Это действительно интересная тема!",
                'friendly': f"Друзья! 😊 Хотите узнать больше о {topic}? Мы подготовили для вас полезную информацию!",
                'formal': f"Уважаемые коллеги, представляем вашему вниманию материал по теме: {topic}."
            }
            
            generated_content = content_templates.get(tone, content_templates['professional'])
            
            hashtags = ['#дизайн', '#UX', '#UI', '#образование'] if 'дизайн' in topic.lower() else ['#бизнес', '#цифровизация', '#автоматизация']
            
            call_to_action = "Подписывайтесь на наш канал для получения полезных материалов!" if platform == 'telegram' else "Следите за нашими обновлениями!"
            
            generated_content = {
                'content': generated_content,
                'hashtags': hashtags,
                'call_to_action': call_to_action,
                'campaign': data.get('campaign'),
                'platform': platform,
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
        
        return jsonify({
            'success': True,
            'data': generated_content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/universal-bot/system-status', methods=['GET'])
@login_required
def get_universal_bot_system_status():
    """Получение статуса системы"""
    try:
        if BOT_INTEGRATION_AVAILABLE:
            # Используем реальные данные от бота
            system_status = bot_integration.get_system_status()
            status_data = asdict(system_status)
        else:
            # Возвращаем тестовые данные
            status_data = {
                'schedulers': {
                    'default': {
                        'status': 'running',
                        'last_run': datetime.now().isoformat(),
                        'next_run': (datetime.now() + timedelta(hours=1)).isoformat(),
                        'error_message': None
                    },
                    'digitalizacija': {
                        'status': 'running',
                        'last_run': datetime.now().isoformat(),
                        'next_run': (datetime.now() + timedelta(hours=1)).isoformat(),
                        'error_message': None
                    }
                },
                'content_generator': {
                    'status': 'available',
                    'last_generation': datetime.now().isoformat(),
                    'error_message': None
                },
                'database': {
                    'status': 'connected',
                    'last_backup': datetime.now().isoformat()
                },
                'telegram_api': {
                    'status': 'connected',
                    'last_check': datetime.now().isoformat()
                }
            }
        
        return jsonify({
            'success': True,
            'data': status_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===== МАРШРУТЫ ДЛЯ УНИВЕРСАЛЬНОГО БОТА =====

@app.route('/universal-bot')
@login_required
def universal_bot_dashboard():
    """Дашборд универсального бота"""
    return render_template('universal_bot_dashboard.html')

@app.route('/universal-bot/campaigns')
@login_required
def universal_bot_campaigns():
    """Управление кампаниями"""
    return render_template('universal_bot_campaigns.html')

@app.route('/universal-bot/posts')
@login_required
def universal_bot_posts():
    """Управление постами"""
    return render_template('universal_bot_posts.html')

@app.route('/universal-bot/generator')
@login_required
def universal_bot_generator():
    """Генератор контента"""
    return render_template('universal_bot_generator.html')

@app.route('/manage-courses')
@login_required
def manage_courses():
    return render_template('manage_courses.html')

@app.route('/manage-team')
@login_required
def manage_team():
    return render_template('manage_team.html')

@app.route('/manage-campaigns')
@login_required
def manage_campaigns():
    return render_template('manage_campaigns.html')

@app.route('/student-analytics')
@login_required
def student_analytics():
    return render_template('student_analytics.html')

@app.route('/financial-report')
@login_required
def financial_report():
    return render_template('financial_report.html')

@app.route('/partner-program')
@login_required
def partner_program():
    return render_template('partner_program.html')

@app.route('/telegram-bot')
@login_required
def telegram_bot():
    return render_template('telegram_bot_dashboard.html')

@app.route('/content-generator')
@login_required
def content_generator():
    return render_template('content_generator_dashboard.html')

# ... existing code ...

if __name__ == '__main__':
    init_db() # Вызываем инициализацию БД при старте
    # Запускаем сервер на порту 5001, чтобы не конфликтовать с другими сервисами
    app.run(debug=True, port=5001) 