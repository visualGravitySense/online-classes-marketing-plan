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

if __name__ == '__main__':
    # Запускаем сервер на порту 5001, чтобы не конфликтовать с другими сервисами
    app.run(debug=True, port=5001) 