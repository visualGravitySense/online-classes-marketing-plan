#!/usr/bin/env python3
"""
Скрипт для создания каналов и групп для кампании "Digitalizacija Biznesa"
"""

import telebot
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class ChannelCreator:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.admin_id = int(os.getenv('ADMIN_ID', 0))
        self.bot = telebot.TeleBot(self.bot_token)
        
        # Конфигурация каналов для создания
        self.channels_to_create = {
            'digitalizacija_main': {
                'title': 'Digitalizacija Biznesa',
                'description': '🚀 Основной канал курса по цифровизации бизнеса\n\n'
                              '📊 Автоматизация процессов\n'
                              '💻 CRM-системы\n'
                              '📈 Цифровой маркетинг\n'
                              '📊 Аналитика и метрики\n'
                              '🚀 Масштабирование бизнеса\n\n'
                              '💡 Практические кейсы и советы от экспертов\n'
                              '🎯 Пошаговые инструкции\n'
                              '📚 Бесплатные материалы\n\n'
                              '🔗 Ссылка на курс: @digitalizacija_bot',
                'type': 'channel',
                'username': 'digitalizacija_biznesa'
            },
            'biznes_automation': {
                'title': 'Biznes Automation',
                'description': '⚙️ Кейсы автоматизации бизнес-процессов\n\n'
                              '🤖 Чат-боты для бизнеса\n'
                              '📧 Email-маркетинг\n'
                              '📊 CRM и ERP системы\n'
                              '🔄 Автоматизация рутинных задач\n'
                              '📈 Инструменты для роста\n\n'
                              '💼 Реальные примеры внедрения\n'
                              '📋 Чек-листы и гайды\n'
                              '🎯 ROI от автоматизации',
                'type': 'channel',
                'username': 'biznes_automation'
            },
            'startup_digital': {
                'title': 'Startup Digital',
                'description': '🚀 Цифровизация для стартапов и предпринимателей\n\n'
                              '💡 Идеи для цифрового бизнеса\n'
                              '📱 Мобильные приложения\n'
                              '🌐 Веб-платформы\n'
                              '📊 Аналитика стартапов\n'
                              '💰 Привлечение инвестиций\n\n'
                              '🎯 Стратегии роста\n'
                              '📈 Метрики успеха\n'
                              '🤝 Нетворкинг',
                'type': 'channel',
                'username': 'startup_digital'
            }
        }
        
        # Конфигурация групп для создания
        self.groups_to_create = {
            'digitalizacija_community': {
                'title': 'Digitalizacija Community',
                'description': '👥 Основная группа участников курса "Digitalizacija Biznesa"\n\n'
                              '💬 Обсуждение тем курса\n'
                              '🤝 Нетворкинг\n'
                              '📚 Обмен опытом\n'
                              '❓ Вопросы и ответы\n'
                              '🎯 Поддержка участников\n\n'
                              '📢 Анонсы новых уроков\n'
                              '🎁 Бонусные материалы\n'
                              '🏆 Истории успеха',
                'type': 'group',
                'username': 'digitalizacija_community'
            },
            'biznes_consulting': {
                'title': 'Biznes Consulting',
                'description': '💼 Группа консультаций по цифровизации бизнеса\n\n'
                              '🎯 Персональные консультации\n'
                              '📊 Аудит процессов\n'
                              '💡 Рекомендации по автоматизации\n'
                              '📈 Стратегии роста\n'
                              '🔧 Техническая поддержка\n\n'
                              '👨‍💼 Эксперты в области цифровизации\n'
                              '📋 Индивидуальные планы\n'
                              '🚀 Результаты клиентов',
                'type': 'group',
                'username': 'biznes_consulting'
            },
            'automation_tips': {
                'title': 'Automation Tips',
                'description': '💡 Советы по автоматизации бизнеса\n\n'
                              '⚙️ Инструменты автоматизации\n'
                              '📋 Пошаговые инструкции\n'
                              '🎯 Лайфхаки и трюки\n'
                              '📊 Обзоры сервисов\n'
                              '🔧 Настройка интеграций\n\n'
                              '💬 Обсуждение инструментов\n'
                              '❓ Помощь в настройке\n'
                              '📚 Библиотека ресурсов',
                'type': 'group',
                'username': 'automation_tips'
            }
        }
    
    def create_channel(self, channel_config):
        """Создание канала"""
        try:
            # Создаем канал
            result = self.bot.create_channel(
                title=channel_config['title'],
                description=channel_config['description']
            )
            
            if result:
                print(f"✅ Канал '{channel_config['title']}' создан успешно!")
                print(f"   ID: {result.chat.id}")
                print(f"   Username: @{channel_config['username']}")
                return result.chat.id
            else:
                print(f"❌ Ошибка при создании канала '{channel_config['title']}'")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при создании канала '{channel_config['title']}': {e}")
            return None
    
    def create_group(self, group_config):
        """Создание группы"""
        try:
            # Создаем группу
            result = self.bot.create_group(
                title=group_config['title'],
                description=group_config['description']
            )
            
            if result:
                print(f"✅ Группа '{group_config['title']}' создана успешно!")
                print(f"   ID: {result.chat.id}")
                print(f"   Username: @{group_config['username']}")
                return result.chat.id
            else:
                print(f"❌ Ошибка при создании группы '{group_config['title']}'")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при создании группы '{group_config['title']}': {e}")
            return None
    
    def set_channel_username(self, chat_id, username):
        """Установка username для канала"""
        try:
            result = self.bot.set_chat_username(chat_id, username)
            if result:
                print(f"✅ Username @{username} установлен для канала")
            else:
                print(f"❌ Ошибка при установке username @{username}")
        except Exception as e:
            print(f"❌ Ошибка при установке username @{username}: {e}")
    
    def set_group_username(self, chat_id, username):
        """Установка username для группы"""
        try:
            result = self.bot.set_chat_username(chat_id, username)
            if result:
                print(f"✅ Username @{username} установлен для группы")
            else:
                print(f"❌ Ошибка при установке username @{username}")
        except Exception as e:
            print(f"❌ Ошибка при установке username @{username}: {e}")
    
    def add_bot_to_channel(self, chat_id):
        """Добавление бота в канал как администратора"""
        try:
            # Добавляем бота как администратора
            result = self.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=self.bot.get_me().id,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False
            )
            
            if result:
                print(f"✅ Бот добавлен как администратор в канал {chat_id}")
            else:
                print(f"❌ Ошибка при добавлении бота в канал {chat_id}")
                
        except Exception as e:
            print(f"❌ Ошибка при добавлении бота в канал {chat_id}: {e}")
    
    def add_bot_to_group(self, chat_id):
        """Добавление бота в группу как администратора"""
        try:
            # Добавляем бота как администратора
            result = self.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=self.bot.get_me().id,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False
            )
            
            if result:
                print(f"✅ Бот добавлен как администратор в группу {chat_id}")
            else:
                print(f"❌ Ошибка при добавлении бота в группу {chat_id}")
                
        except Exception as e:
            print(f"❌ Ошибка при добавлении бота в группу {chat_id}: {e}")
    
    def save_channel_ids(self, channel_ids):
        """Сохранение ID каналов в файл"""
        try:
            with open('digitalizacija_channel_ids.json', 'w', encoding='utf-8') as f:
                json.dump(channel_ids, f, indent=2, ensure_ascii=False)
            print("✅ ID каналов сохранены в файл digitalizacija_channel_ids.json")
        except Exception as e:
            print(f"❌ Ошибка при сохранении ID каналов: {e}")
    
    def create_all_channels(self):
        """Создание всех каналов и групп"""
        print("🚀 Начинаем создание каналов и групп для кампании 'Digitalizacija Biznesa'")
        print("=" * 60)
        
        channel_ids = {}
        
        # Создаем каналы
        print("\n📺 СОЗДАНИЕ КАНАЛОВ:")
        print("-" * 30)
        
        for channel_key, channel_config in self.channels_to_create.items():
            print(f"\nСоздаем канал: {channel_config['title']}")
            chat_id = self.create_channel(channel_config)
            
            if chat_id:
                channel_ids[channel_key] = {
                    'chat_id': chat_id,
                    'username': channel_config['username'],
                    'title': channel_config['title']
                }
                
                # Устанавливаем username
                self.set_channel_username(chat_id, channel_config['username'])
                
                # Добавляем бота как администратора
                self.add_bot_to_channel(chat_id)
        
        # Создаем группы
        print("\n\n👥 СОЗДАНИЕ ГРУПП:")
        print("-" * 30)
        
        for group_key, group_config in self.groups_to_create.items():
            print(f"\nСоздаем группу: {group_config['title']}")
            chat_id = self.create_group(group_config)
            
            if chat_id:
                channel_ids[group_key] = {
                    'chat_id': chat_id,
                    'username': group_config['username'],
                    'title': group_config['title']
                }
                
                # Устанавливаем username
                self.set_group_username(chat_id, group_config['username'])
                
                # Добавляем бота как администратора
                self.add_bot_to_group(chat_id)
        
        # Сохраняем ID каналов
        print("\n\n💾 СОХРАНЕНИЕ РЕЗУЛЬТАТОВ:")
        print("-" * 30)
        self.save_channel_ids(channel_ids)
        
        # Выводим итоговую информацию
        print("\n\n📋 ИТОГОВАЯ ИНФОРМАЦИЯ:")
        print("-" * 30)
        print("Созданные каналы и группы:")
        
        for key, info in channel_ids.items():
            print(f"  {key}:")
            print(f"    ID: {info['chat_id']}")
            print(f"    Username: @{info['username']}")
            print(f"    Название: {info['title']}")
            print()
        
        print("🎉 Создание каналов и групп завершено!")
        print("\n📝 Следующие шаги:")
        print("1. Добавьте ID каналов в .env файл")
        print("2. Настройте права доступа для бота")
        print("3. Добавьте приветственные посты")
        print("4. Настройте автоматическое постинг")
        
        return channel_ids

def main():
    """Основная функция"""
    creator = ChannelCreator()
    channel_ids = creator.create_all_channels()
    
    # Создаем .env файл с новыми переменными
    env_content = f"""
# ID каналов для кампании "Digitalizacija Biznesa"
DIGITALIZACIJA_MAIN_CHANNEL_ID={channel_ids.get('digitalizacija_main', {}).get('chat_id', '')}
BIZNES_AUTOMATION_CHANNEL_ID={channel_ids.get('biznes_automation', {}).get('chat_id', '')}
STARTUP_DIGITAL_CHANNEL_ID={channel_ids.get('startup_digital', {}).get('chat_id', '')}

# ID групп для кампании "Digitalizacija Biznesa"
DIGITALIZACIJA_COMMUNITY_ID={channel_ids.get('digitalizacija_community', {}).get('chat_id', '')}
BIZNES_CONSULTING_ID={channel_ids.get('biznes_consulting', {}).get('chat_id', '')}
AUTOMATION_TIPS_ID={channel_ids.get('automation_tips', {}).get('chat_id', '')}
"""
    
    try:
        with open('digitalizacija_env.txt', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("\n✅ Создан файл digitalizacija_env.txt с переменными окружения")
        print("   Добавьте эти переменные в ваш .env файл")
    except Exception as e:
        print(f"❌ Ошибка при создании файла с переменными: {e}")

if __name__ == "__main__":
    main() 