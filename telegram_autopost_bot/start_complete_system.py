#!/usr/bin/env python3
"""
Главный скрипт для запуска полной системы кампании "Digitalizacija Biznesa"
Включает: постинг, лидогенерацию, аналитику
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from welcome_posts import WelcomePostsManager
from digitalizacija_scheduler import DigitalizacijaScheduler
from lead_generation_bot import LeadGenerationBot
from analytics_system import AnalyticsSystem
from config import DIGITALIZACIJA_CHANNELS

load_dotenv()

class CompleteDigitalizacijaSystem:
    def __init__(self):
        self.system_name = "Digitalizacija Biznesa"
        self.version = "2.0.0"
        
        # Проверяем окружение
        self.check_environment()
        
        # Инициализируем компоненты
        self.welcome_manager = WelcomePostsManager()
        self.scheduler = DigitalizacijaScheduler()
        self.lead_bot = LeadGenerationBot()
        self.analytics = AnalyticsSystem()
        
        # Статус компонентов
        self.components_status = {
            'scheduler': False,
            'lead_bot': False,
            'analytics': False
        }
    
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
            with open('digitalizacija_channel_ids.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
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
    
    def initialize_system(self):
        """Инициализация системы"""
        print("\n🚀 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ")
        print("=" * 50)
        
        # 1. Отправляем приветственные посты
        print("\n1️⃣ Отправка приветственных постов...")
        channel_ids = self.load_channel_ids()
        welcome_results = self.welcome_manager.send_all_welcome_posts(channel_ids)
        
        success_count = sum(1 for r in welcome_results.values() if r['status'] == 'success')
        total_count = len(welcome_results)
        print(f"   Результат: {success_count}/{total_count} успешно")
        
        # 2. Настраиваем планировщик
        print("\n2️⃣ Настройка планировщика...")
        try:
            self.scheduler.create_test_posts()
            self.scheduler.schedule_weekly_content()
            self.components_status['scheduler'] = True
            print("   ✅ Планировщик настроен")
        except Exception as e:
            print(f"   ❌ Ошибка настройки планировщика: {e}")
        
        # 3. Генерируем первый отчет
        print("\n3️⃣ Генерация первого отчета...")
        try:
            self.analytics.generate_daily_report()
            print("   ✅ Отчет сгенерирован")
        except Exception as e:
            print(f"   ❌ Ошибка генерации отчета: {e}")
        
        print("\n✅ Инициализация завершена")
    
    def start_scheduler(self):
        """Запуск планировщика в отдельном потоке"""
        def run_scheduler():
            try:
                self.scheduler.run_scheduler()
            except Exception as e:
                print(f"❌ Ошибка планировщика: {e}")
                self.components_status['scheduler'] = False
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        self.components_status['scheduler'] = True
        print("✅ Планировщик запущен")
    
    def start_lead_bot(self):
        """Запуск бота лидогенерации в отдельном потоке"""
        def run_lead_bot():
            try:
                self.lead_bot.run()
            except Exception as e:
                print(f"❌ Ошибка бота лидогенерации: {e}")
                self.components_status['lead_bot'] = False
        
        lead_bot_thread = threading.Thread(target=run_lead_bot, daemon=True)
        lead_bot_thread.start()
        self.components_status['lead_bot'] = True
        print("✅ Бот лидогенерации запущен")
    
    def start_analytics(self):
        """Запуск системы аналитики в отдельном потоке"""
        def run_analytics():
            try:
                self.analytics.run_scheduler()
            except Exception as e:
                print(f"❌ Ошибка системы аналитики: {e}")
                self.components_status['analytics'] = False
        
        analytics_thread = threading.Thread(target=run_analytics, daemon=True)
        analytics_thread.start()
        self.components_status['analytics'] = True
        print("✅ Система аналитики запущена")
    
    def show_status(self):
        """Показ статуса системы"""
        print("\n📊 СТАТУС СИСТЕМЫ")
        print("=" * 50)
        
        status_icons = {True: "✅", False: "❌"}
        
        for component, status in self.components_status.items():
            icon = status_icons[status]
            print(f"{icon} {component}: {'Активен' if status else 'Неактивен'}")
        
        # Показываем статистику
        try:
            leads_stats = self.analytics.get_leads_statistics(days=7)
            posts_stats = self.analytics.get_posts_statistics(days=7)
            
            print(f"\n📈 Статистика за неделю:")
            print(f"   Лидов: {leads_stats['recent_leads']}")
            print(f"   Постов: {posts_stats['posts_stats'].iloc[0]['sent_posts']}")
            print(f"   Просмотров: {posts_stats['engagement_stats'].iloc[0]['total_views'] or 0}")
            
        except Exception as e:
            print(f"   ❌ Ошибка получения статистики: {e}")
    
    def show_menu(self):
        """Показ меню управления"""
        print("\n🎛️ МЕНЮ УПРАВЛЕНИЯ")
        print("=" * 50)
        print("1. Показать статус системы")
        print("2. Отправить приветственные посты")
        print("3. Создать тестовые посты")
        print("4. Генерировать отчет")
        print("5. Показать статистику")
        print("6. Перезапустить компонент")
        print("7. Выход")
        print("-" * 50)
    
    def restart_component(self, component_name):
        """Перезапуск компонента"""
        print(f"\n🔄 Перезапуск {component_name}...")
        
        if component_name == 'scheduler':
            self.components_status['scheduler'] = False
            time.sleep(2)
            self.start_scheduler()
        elif component_name == 'lead_bot':
            self.components_status['lead_bot'] = False
            time.sleep(2)
            self.start_lead_bot()
        elif component_name == 'analytics':
            self.components_status['analytics'] = False
            time.sleep(2)
            self.start_analytics()
        
        print(f"✅ {component_name} перезапущен")
    
    def run_interactive(self):
        """Интерактивный режим"""
        print(f"🚀 Полная система {self.system_name} v{self.version}")
        print("=" * 60)
        
        # Инициализируем систему
        self.initialize_system()
        
        # Запускаем все компоненты
        print("\n🚀 ЗАПУСК КОМПОНЕНТОВ")
        print("=" * 50)
        
        self.start_scheduler()
        self.start_lead_bot()
        self.start_analytics()
        
        print("\n🎉 Все компоненты запущены!")
        print("Система работает в автоматическом режиме")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Выберите действие (1-7): ").strip()
                
                if choice == '1':
                    self.show_status()
                    
                elif choice == '2':
                    print("\n📝 Отправка приветственных постов...")
                    channel_ids = self.load_channel_ids()
                    self.welcome_manager.send_all_welcome_posts(channel_ids)
                    
                elif choice == '3':
                    print("\n🧪 Создание тестовых постов...")
                    self.scheduler.create_test_posts()
                    
                elif choice == '4':
                    print("\n📊 Генерация отчета...")
                    report_type = input("Тип отчета (daily/weekly/monthly): ").strip()
                    
                    if report_type == 'daily':
                        self.analytics.generate_daily_report()
                    elif report_type == 'weekly':
                        self.analytics.generate_weekly_report()
                    elif report_type == 'monthly':
                        self.analytics.generate_monthly_report()
                    else:
                        print("❌ Неверный тип отчета")
                    
                elif choice == '5':
                    self.show_status()
                    
                elif choice == '6':
                    print("\n🔄 Перезапуск компонента...")
                    print("1. Планировщик")
                    print("2. Бот лидогенерации")
                    print("3. Система аналитики")
                    
                    component_choice = input("Выберите компонент (1-3): ").strip()
                    
                    if component_choice == '1':
                        self.restart_component('scheduler')
                    elif component_choice == '2':
                        self.restart_component('lead_bot')
                    elif component_choice == '3':
                        self.restart_component('analytics')
                    else:
                        print("❌ Неверный выбор")
                    
                elif choice == '7':
                    print("\n👋 Завершение работы системы...")
                    break
                    
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Завершение работы системы...")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def run_automatic(self):
        """Автоматический режим"""
        print(f"🚀 Автоматический запуск системы {self.system_name}")
        print("=" * 60)
        
        # Инициализируем систему
        self.initialize_system()
        
        # Запускаем все компоненты
        print("\n🚀 ЗАПУСК КОМПОНЕНТОВ")
        print("=" * 50)
        
        self.start_scheduler()
        self.start_lead_bot()
        self.start_analytics()
        
        print("\n🎉 Система работает в автоматическом режиме!")
        print("Для остановки нажмите Ctrl+C")
        
        try:
            # Показываем статус каждые 5 минут
            while True:
                time.sleep(300)  # 5 минут
                self.show_status()
                
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
    
    parser = argparse.ArgumentParser(description='Полная система кампании "Digitalizacija Biznesa"')
    parser.add_argument('--mode', choices=['interactive', 'automatic'], 
                       default='interactive', help='Режим работы')
    parser.add_argument('--init-only', action='store_true', 
                       help='Только инициализация системы')
    parser.add_argument('--status-only', action='store_true', 
                       help='Только показ статуса')
    
    args = parser.parse_args()
    
    system = CompleteDigitalizacijaSystem()
    
    if args.init_only:
        print("🚀 Только инициализация системы...")
        system.initialize_system()
    elif args.status_only:
        print("📊 Показ статуса системы...")
        system.show_status()
    else:
        system.run(args.mode)

if __name__ == "__main__":
    main() 