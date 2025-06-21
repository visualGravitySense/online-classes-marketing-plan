# config.py

import os

# Определяем базовую директорию проекта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Путь к основной базе данных
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'posts.db')

# Секретный ключ для Flask. ВАЖНО: для реального продакшена его нужно генерировать
# и хранить более безопасным способом (например, в переменных окружения).
SECRET_KEY = 'dev-secret-key'

# Учетные данные администратора
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password' 