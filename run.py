# run.py
from waitress import serve
from main_api import app

if __name__ == '__main__':
    print("🚀 Starting production server on http://0.0.0.0:8080")
    serve(app, host='0.0.0.0', port=8080) 