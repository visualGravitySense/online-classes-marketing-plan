#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции фронтенда с универсальным ботом
"""

import requests
import json
import time
import sys
from datetime import datetime

# Конфигурация
API_BASE_URL = "http://localhost:5001"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

class IntegrationTester:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = API_BASE_URL
    
    def login(self):
        """Вход в систему"""
        print("🔐 Вход в систему...")
        
        try:
            response = self.session.post(f"{self.base_url}/login", data={
                'username': TEST_USERNAME,
                'password': TEST_PASSWORD
            })
            
            if response.status_code == 200:
                print("✅ Вход выполнен успешно")
                return True
            else:
                print(f"❌ Ошибка входа: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Не удалось подключиться к API серверу")
            print("   Убедитесь, что сервер запущен на http://localhost:5000")
            return False
        except Exception as e:
            print(f"❌ Ошибка входа: {e}")
            return False
    
    def test_dashboard(self):
        """Тест дашборда"""
        print("\n📊 Тест дашборда...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/universal-bot/dashboard")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    dashboard = data['data']
                    print("✅ Дашборд работает")
                    print(f"   Кампаний: {dashboard['campaigns']['total']}")
                    print(f"   Постов: {dashboard['posts']['total']}")
                    print(f"   Каналов: {dashboard['channels']['total']}")
                    return True
                else:
                    print(f"❌ Ошибка дашборда: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста дашборда: {e}")
            return False
    
    def test_campaigns(self):
        """Тест кампаний"""
        print("\n🎯 Тест кампаний...")
        
        try:
            # Получение списка кампаний
            response = self.session.get(f"{self.base_url}/api/universal-bot/campaigns")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    campaigns = data['data']
                    print(f"✅ Получено кампаний: {len(campaigns)}")
                    
                    # Тест создания кампании
                    new_campaign = {
                        'name': f'Тестовая кампания {datetime.now().strftime("%H:%M:%S")}',
                        'description': 'Кампания для тестирования интеграции',
                        'channels': []
                    }
                    
                    response = self.session.post(
                        f"{self.base_url}/api/universal-bot/campaigns",
                        json=new_campaign
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            campaign_id = data['data']['id']
                            print(f"✅ Кампания создана: {campaign_id}")
                            
                            # Тест запуска кампании
                            response = self.session.post(
                                f"{self.base_url}/api/universal-bot/campaigns/{campaign_id}/start"
                            )
                            
                            if response.status_code == 200:
                                print("✅ Кампания запущена")
                            else:
                                print(f"⚠️  Не удалось запустить кампанию: {response.status_code}")
                            
                            return True
                        else:
                            print(f"❌ Ошибка создания кампании: {data.get('error')}")
                            return False
                    else:
                        print(f"❌ Ошибка HTTP при создании: {response.status_code}")
                        return False
                else:
                    print(f"❌ Ошибка получения кампаний: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста кампаний: {e}")
            return False
    
    def test_channels(self):
        """Тест каналов"""
        print("\n📢 Тест каналов...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/universal-bot/channels")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    channels = data['data']
                    print(f"✅ Получено каналов: {len(channels)}")
                    
                    for channel in channels[:3]:  # Показываем первые 3
                        print(f"   - {channel['name']} ({channel['status']})")
                    
                    return True
                else:
                    print(f"❌ Ошибка получения каналов: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста каналов: {e}")
            return False
    
    def test_posts(self):
        """Тест постов"""
        print("\n📝 Тест постов...")
        
        try:
            # Получение списка постов
            response = self.session.get(f"{self.base_url}/api/universal-bot/posts")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    posts = data['data']
                    print(f"✅ Получено постов: {len(posts)}")
                    
                    # Тест создания поста
                    new_post = {
                        'content': f'Тестовый пост {datetime.now().strftime("%H:%M:%S")} - проверка интеграции!',
                        'campaign': 'default',
                        'channels': []
                    }
                    
                    response = self.session.post(
                        f"{self.base_url}/api/universal-bot/posts",
                        json=new_post
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            post_id = data['data']['id']
                            print(f"✅ Пост создан: {post_id}")
                            return True
                        else:
                            print(f"❌ Ошибка создания поста: {data.get('error')}")
                            return False
                    else:
                        print(f"❌ Ошибка HTTP при создании поста: {response.status_code}")
                        return False
                else:
                    print(f"❌ Ошибка получения постов: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста постов: {e}")
            return False
    
    def test_content_generator(self):
        """Тест генератора контента"""
        print("\n✨ Тест генератора контента...")
        
        try:
            content_request = {
                'topic': 'UX/UI дизайн для начинающих',
                'campaign': 'default',
                'tone': 'friendly',
                'length': 'medium',
                'target_audience': 'начинающие дизайнеры',
                'platform': 'telegram',
                'include_hashtags': True,
                'include_call_to_action': True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/universal-bot/generate-content",
                json=content_request
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    content = data['data']
                    print("✅ Контент сгенерирован")
                    print(f"   Длина: {len(content['content'])} символов")
                    print(f"   Хештеги: {len(content.get('hashtags', []))}")
                    print(f"   Призыв к действию: {'Да' if content.get('call_to_action') else 'Нет'}")
                    return True
                else:
                    print(f"❌ Ошибка генерации: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста генератора: {e}")
            return False
    
    def test_system_status(self):
        """Тест статуса системы"""
        print("\n⚙️  Тест статуса системы...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/universal-bot/system-status")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status = data['data']
                    print("✅ Статус системы получен")
                    
                    # Проверяем компоненты
                    schedulers = status.get('schedulers', {})
                    print(f"   Планировщики: {len(schedulers)}")
                    
                    content_gen = status.get('content_generator', {})
                    print(f"   Генератор контента: {content_gen.get('status', 'unknown')}")
                    
                    database = status.get('database', {})
                    print(f"   База данных: {database.get('status', 'unknown')}")
                    
                    telegram_api = status.get('telegram_api', {})
                    print(f"   Telegram API: {telegram_api.get('status', 'unknown')}")
                    
                    return True
                else:
                    print(f"❌ Ошибка получения статуса: {data.get('error')}")
                    return False
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка теста статуса: {e}")
            return False
    
    def test_frontend_pages(self):
        """Тест фронтенд страниц"""
        print("\n🌐 Тест фронтенд страниц...")
        
        pages = [
            '/universal-bot',
            '/universal-bot/campaigns',
            '/universal-bot/posts',
            '/universal-bot/generator'
        ]
        
        success_count = 0
        
        for page in pages:
            try:
                response = self.session.get(f"{self.base_url}{page}")
                
                if response.status_code == 200:
                    print(f"✅ {page} - доступна")
                    success_count += 1
                else:
                    print(f"❌ {page} - ошибка {response.status_code}")
            except Exception as e:
                print(f"❌ {page} - ошибка: {e}")
        
        return success_count == len(pages)
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("🧪 Запуск тестов интеграции")
        print("=" * 50)
        
        # Вход в систему
        if not self.login():
            return False
        
        # Список тестов
        tests = [
            ("Дашборд", self.test_dashboard),
            ("Кампании", self.test_campaigns),
            ("Каналы", self.test_channels),
            ("Посты", self.test_posts),
            ("Генератор контента", self.test_content_generator),
            ("Статус системы", self.test_system_status),
            ("Фронтенд страницы", self.test_frontend_pages)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Ошибка в тесте {test_name}: {e}")
                results.append((test_name, False))
        
        # Вывод результатов
        print("\n" + "=" * 50)
        print("📋 РЕЗУЛЬТАТЫ ТЕСТОВ")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
            print(f"{test_name:<25} {status}")
            if result:
                passed += 1
        
        print("=" * 50)
        print(f"Итого: {passed}/{total} тестов пройдено")
        
        if passed == total:
            print("🎉 Все тесты пройдены! Интеграция работает корректно.")
        else:
            print("⚠️  Некоторые тесты не пройдены. Проверьте конфигурацию.")
        
        return passed == total

def main():
    """Основная функция"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print("""
🧪 Тест интеграции фронтенда с универсальным ботом

Использование:
    python test_integration.py

Требования:
    - Запущенный API сервер на http://localhost:5000
    - Настроенная конфигурация бота
    - Доступ к базе данных

Тесты:
    - Вход в систему
    - Дашборд
    - Управление кампаниями
    - Управление каналами
    - Управление постами
    - Генератор контента
    - Статус системы
    - Фронтенд страницы
        """)
        return
    
    tester = IntegrationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Система готова к использованию!")
        print("   Откройте http://localhost:5000 в браузере")
    else:
        print("\n🔧 Требуется настройка системы")
        print("   Проверьте конфигурацию и логи")

if __name__ == "__main__":
    main() 