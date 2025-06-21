#!/usr/bin/env python3
"""
Тестовый скрипт для проверки генерации контента и интеграции с Telegram ботом
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Конфигурация
API_BASE_URL = "http://localhost:8000"
TEST_CHANNEL_ID = "-1001234567890"  # Замените на реальный ID канала

def test_api_connection():
    """Тестирует подключение к API"""
    print("🔍 Тестирование подключения к API...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats")
        if response.status_code == 200:
            print("✅ API подключение успешно")
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_content_generation():
    """Тестирует генерацию контента"""
    print("\n🎨 Тестирование генерации контента...")
    
    audiences = ["Новички в дизайне", "Junior дизайнеры", "Фрилансеры", "Разработчики"]
    content_types = ["Проблема", "Решение", "Преимущества курса", "Кейс", "Совет", "Мотивация"]
    
    for audience in audiences:
        print(f"\n📊 Тестируем аудиторию: {audience}")
        for content_type in content_types:
            try:
                response = requests.post(f"{API_BASE_URL}/api/content/generate", json={
                    "audience_group": audience,
                    "content_type": content_type,
                    "channel_id": TEST_CHANNEL_ID,
                    "custom_prompt": ""
                })
                
                if response.status_code == 200:
                    data = response.json()
                    if data["status"] == "success":
                        print(f"  ✅ {content_type}: OK")
                        # Показываем пример контента
                        if audience == "Новички в дизайне" and content_type == "Проблема":
                            print(f"     Пример: {data['content'][:100]}...")
                    else:
                        print(f"  ❌ {content_type}: {data.get('detail', 'Unknown error')}")
                else:
                    print(f"  ❌ {content_type}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {content_type}: {e}")
            
            time.sleep(0.5)  # Небольшая пауза между запросами

def test_batch_generation():
    """Тестирует пакетную генерацию"""
    print("\n📦 Тестирование пакетной генерации...")
    
    try:
        # Генерируем 3 поста для каждой аудитории
        for audience in ["Новички в дизайне", "Junior дизайнеры"]:
            print(f"\n🎯 Генерируем пакет для: {audience}")
            
            posts = []
            for i in range(3):
                response = requests.post(f"{API_BASE_URL}/api/content/generate", json={
                    "audience_group": audience,
                    "content_type": "Проблема",  # Простой тип для теста
                    "channel_id": TEST_CHANNEL_ID,
                    "custom_prompt": ""
                })
                
                if response.status_code == 200:
                    data = response.json()
                    if data["status"] == "success":
                        posts.append(data["content"])
                        print(f"  ✅ Пост {i+1} сгенерирован")
                    else:
                        print(f"  ❌ Пост {i+1}: {data.get('detail', 'Error')}")
                else:
                    print(f"  ❌ Пост {i+1}: HTTP {response.status_code}")
                
                time.sleep(0.5)
            
            print(f"  📊 Всего сгенерировано: {len(posts)} постов")
            
    except Exception as e:
        print(f"❌ Ошибка пакетной генерации: {e}")

def test_content_publishing():
    """Тестирует публикацию контента"""
    print("\n🚀 Тестирование публикации контента...")
    
    try:
        # Планируем пост на завтра
        tomorrow = datetime.now() + timedelta(days=1)
        
        response = requests.post(f"{API_BASE_URL}/api/content/publish", json={
            "audience_group": "Новички в дизайне",
            "content_type": "Проблема",
            "channel_id": TEST_CHANNEL_ID,
            "scheduled_time": tomorrow.isoformat(),
            "custom_prompt": "Тестовый пост для проверки системы"
        })
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print(f"✅ Контент опубликован! ID поста: {data['post_id']}")
                print(f"📅 Запланировано на: {tomorrow.strftime('%Y-%m-%d %H:%M')}")
                return data['post_id']
            else:
                print(f"❌ Ошибка публикации: {data.get('detail', 'Unknown error')}")
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка публикации: {e}")
    
    return None

def test_analytics():
    """Тестирует аналитику контента"""
    print("\n📊 Тестирование аналитики...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/content/analytics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Аналитика загружена:")
            print(f"   📝 Всего постов: {data['total_posts']}")
            print(f"   ✅ Опубликовано: {data['published_posts']}")
            print(f"   ❌ Ошибок: {data['failed_posts']}")
            print(f"   📈 Успешность: {data['success_rate']:.1f}%")
        else:
            print(f"❌ Ошибка загрузки аналитики: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка аналитики: {e}")

def test_dashboard_integration():
    """Тестирует интеграцию с дашбордом"""
    print("\n🖥️ Тестирование интеграции с дашбордом...")
    
    try:
        # Проверяем доступность дашборда
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ Дашборд доступен")
        else:
            print(f"❌ Дашборд недоступен: {response.status_code}")
            
        # Проверяем API endpoints для дашборда
        endpoints = [
            "/api/channels",
            "/api/content/audiences", 
            "/api/content/types"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{API_BASE_URL}{endpoint}")
                if response.status_code == 200:
                    print(f"  ✅ {endpoint}: OK")
                else:
                    print(f"  ❌ {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"  ❌ {endpoint}: {e}")
                
    except Exception as e:
        print(f"❌ Ошибка тестирования дашборда: {e}")

def main():
    """Основная функция тестирования"""
    print("🧪 Запуск тестирования системы генерации контента")
    print("=" * 60)
    
    # Проверяем подключение
    if not test_api_connection():
        print("\n❌ Не удалось подключиться к API. Убедитесь, что сервер запущен.")
        return
    
    # Запускаем все тесты
    test_content_generation()
    test_batch_generation()
    post_id = test_content_publishing()
    test_analytics()
    test_dashboard_integration()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование завершено!")
    
    if post_id:
        print(f"📝 Тестовый пост создан с ID: {post_id}")
    
    print("\n📋 Следующие шаги:")
    print("1. Откройте дашборд: http://localhost:8000")
    print("2. Перейдите на вкладку 'Генератор контента'")
    print("3. Протестируйте генерацию контента через интерфейс")
    print("4. Проверьте планирование постов")

if __name__ == "__main__":
    main() 