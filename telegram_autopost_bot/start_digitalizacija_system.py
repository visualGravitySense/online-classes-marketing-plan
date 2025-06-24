#!/usr/bin/env python3
"""
Главный скрипт для запуска системы кампании "Digitalizacija Biznesa"
"""

import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from welcome_posts import WelcomePostsManager
from digitalizacija_scheduler import DigitalizacijaScheduler
from config import DIGITALIZACIJA_CHANNELS

load_dotenv()

class DigitalizacijaSystem:
    def __init__(self):
        self.system_name = "Digitalizacija Biznesa"
        self.version = "1.0.0"
        
        # Проверяем наличие необходимых переменных
        self.check_environment()
        
        # Инициализируем компоненты
        self.welcome_manager = WelcomePostsManager()
        self.scheduler = DigitalizacijaScheduler()
    
    def check_environment(self):
        """Проверка переменных окружения"""
        print("🔍 Проверка переменных окружения...")
        
        required_vars = [
            'BOT_TOKEN',
            'ADMIN_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Отсутствуют переменные: {', '.join(missing_vars)}")
            print("Добавьте их в .env файл")
            sys.exit(1)
        
        # Проверяем ID каналов
        channel_vars = [
            'DIGITALIZACIJA_MAIN_CHANNEL_ID',
            'BIZNES_AUTOMATION_CHANNEL_ID',
            'STARTUP_DIGITAL_CHANNEL_ID',
            'DIGITALIZACIJA_COMMUNITY_ID',
            'BIZNES_CONSULTING_ID',
            'AUTOMATION_TIPS_ID'
        ]
        
        missing_channels = []
        for var in channel_vars:
            if not os.getenv(var):
                missing_channels.append(var)
        
        if missing_channels:
            print(f"⚠️ Отсутствуют ID каналов: {', '.join(missing_channels)}")
            print("Создайте каналы или добавьте их ID в .env файл")
        
        print("✅ Проверка окружения завершена")
    
    def load_channel_ids(self):
        """Загрузка ID каналов"""
        try:
            # Пытаемся загрузить из файла
            with open('digitalizacija_channel_ids.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Используем переменные окружения
            return {
                'digitalizacija_main': {
                    'chat_id': os.getenv('DIGITALIZACIJA_MAIN_CHANNEL_ID'),
                    'username': 'digitalizacija_biznesa'
                },
                'biznes_automation': {
                    'chat_id': os.getenv('BIZNES_AUTOMATION_CHANNEL_ID'),
                    'username': 'biznes_automation'
                },
                'startup_digital': {
                    'chat_id': os.getenv('STARTUP_DIGITAL_CHANNEL_ID'),
                    'username': 'startup_digital'
                },
                'digitalizacija_community': {
                    'chat_id': os.getenv('DIGITALIZACIJA_COMMUNITY_ID'),
                    'username': 'digitalizacija_community'
                },
                'biznes_consulting': {
                    'chat_id': os.getenv('BIZNES_CONSULTING_ID'),
                    'username': 'biznes_consulting'
                },
                'automation_tips': {
                    'chat_id': os.getenv('AUTOMATION_TIPS_ID'),
                    'username': 'automation_tips'
                }
            }
    
    def send_welcome_posts(self):
        """Отправка приветственных постов"""
        print("\n📝 ОТПРАВКА ПРИВЕТСТВЕННЫХ ПОСТОВ")
        print("=" * 50)
        
        channel_ids = self.load_channel_ids()
        results = self.welcome_manager.send_all_welcome_posts(channel_ids)
        
        success_count = sum(1 for r in results.values() if r['status'] == 'success')
        total_count = len(results)
        
        print(f"\n📊 Результаты: {success_count}/{total_count} успешно")
        
        return success_count == total_count
    
    def setup_scheduler(self):
        """Настройка планировщика"""
        print("\n⏰ НАСТРОЙКА ПЛАНИРОВЩИКА")
        print("=" * 50)
        
        try:
            # Создаем тестовые посты
            print("🧪 Создание тестовых постов...")
            self.scheduler.create_test_posts()
            
            # Планируем контент на неделю
            print("📅 Планирование контента на неделю...")
            self.scheduler.schedule_weekly_content()
            
            print("✅ Планировщик настроен")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при настройке планировщика: {e}")
            return False
    
    def show_statistics(self):
        """Показ статистики"""
        print("\n📊 СТАТИСТИКА СИСТЕМЫ")
        print("=" * 50)
        
        try:
            stats = self.scheduler.get_statistics()
            
            print(f"📝 Всего постов: {stats['total_posts']}")
            print(f"✅ Отправлено: {stats['sent_posts']}")
            print(f"⏳ Ожидают отправки: {stats['pending_posts']}")
            
            print("\n📈 Статистика по каналам:")
            for channel_id, count in stats['channel_stats']:
                channel_name = "Неизвестный канал"
                for key, info in DIGITALIZACIJA_CHANNELS.items():
                    if info['chat_id'] == channel_id:
                        channel_name = info['name']
                        break
                print(f"  {channel_name}: {count} постов")
            
        except Exception as e:
            print(f"❌ Ошибка при получении статистики: {e}")
    
    def show_menu(self):
        """Показ меню управления"""
        print("\n🎛️ МЕНЮ УПРАВЛЕНИЯ")
        print("=" * 50)
        print("1. Отправить приветственные посты")
        print("2. Настроить планировщик")
        print("3. Показать статистику")
        print("4. Запустить планировщик")
        print("5. Создать тестовые посты")
        print("6. Выход")
        print("-" * 50)
    
    def run_interactive(self):
        """Интерактивный режим"""
        print(f"🚀 Система {self.system_name} v{self.version}")
        print("=" * 60)
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Выберите действие (1-6): ").strip()
                
                if choice == '1':
                    self.send_welcome_posts()
                    
                elif choice == '2':
                    self.setup_scheduler()
                    
                elif choice == '3':
                    self.show_statistics()
                    
                elif choice == '4':
                    print("\n🚀 Запуск планировщика...")
                    print("Для остановки нажмите Ctrl+C")
                    try:
                        self.scheduler.run_scheduler()
                    except KeyboardInterrupt:
                        print("\n⏹️ Планировщик остановлен")
                    
                elif choice == '5':
                    print("\n🧪 Создание тестовых постов...")
                    self.scheduler.create_test_posts()
                    
                elif choice == '6':
                    print("\n👋 До свидания!")
                    break
                    
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def run_automatic(self):
        """Автоматический режим"""
        print(f"🚀 Автоматический запуск системы {self.system_name}")
        print("=" * 60)
        
        # Отправляем приветственные посты
        print("\n1️⃣ Отправка приветственных постов...")
        if not self.send_welcome_posts():
            print("⚠️ Некоторые посты не были отправлены")
        
        # Настраиваем планировщик
        print("\n2️⃣ Настройка планировщика...")
        if not self.setup_scheduler():
            print("❌ Ошибка при настройке планировщика")
            return
        
        # Показываем статистику
        print("\n3️⃣ Статистика системы...")
        self.show_statistics()
        
        # Запускаем планировщик
        print("\n4️⃣ Запуск планировщика...")
        print("Система работает в автоматическом режиме")
        print("Для остановки нажмите Ctrl+C")
        
        try:
            self.scheduler.run_scheduler()
        except KeyboardInterrupt:
            print("\n⏹️ Система остановлена")
    
    def run(self, mode='interactive'):
        """Запуск системы"""
        if mode == 'automatic':
            self.run_automatic()
        else:
            self.run_interactive()

def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Система кампании "Digitalizacija Biznesa"')
    parser.add_argument('--mode', choices=['interactive', 'automatic'], 
                       default='interactive', help='Режим работы')
    parser.add_argument('--welcome-only', action='store_true', 
                       help='Только отправить приветственные посты')
    parser.add_argument('--setup-only', action='store_true', 
                       help='Только настроить планировщик')
    
    args = parser.parse_args()
    
    system = DigitalizacijaSystem()
    
    if args.welcome_only:
        print("📝 Отправка только приветственных постов...")
        system.send_welcome_posts()
    elif args.setup_only:
        print("⏰ Только настройка планировщика...")
        system.setup_scheduler()
    else:
        system.run(args.mode)

if __name__ == "__main__":
    main() 