#!/usr/bin/env python3
"""
Универсальный Telegram бот для автопостинга
Поддерживает множественные направления/кампании:
- UXUI дизайн (default)
- Цифровизация бизнеса (digitalizacija)
- Легко добавлять новые направления
"""

import logging
import os
import sys
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import asyncio

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем из локального config.py
from config import BOT_TOKEN, ADMIN_ID, ALL_CHANNELS, POSTING_SCHEDULE, POST_TEMPLATES
from database import Database
from scheduler import PostScheduler
from integrated_content_generator import ContentGenerator

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CampaignStates(StatesGroup):
    """Состояния для управления кампаниями"""
    choosing_campaign = State()
    choosing_action = State()
    choosing_channel = State()
    entering_content = State()
    entering_media = State()
    entering_time = State()

class UniversalBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.db = Database('data/posts.db')
        self.content_generator = ContentGenerator()
        
        # Статус компонентов (инициализируем ПЕРЕД планировщиками)
        self.components_status = {
            'schedulers': {},
            'content_generator': False
        }
        
        # Инициализируем планировщики для каждой кампании
        self.schedulers = {}
        self.initialize_schedulers()
        
        # Регистрируем обработчики команд
        self.register_handlers()
    
    def initialize_schedulers(self):
        """Инициализация планировщиков для каждой кампании"""
        campaigns = self.get_available_campaigns()
        
        for campaign in campaigns:
            campaign_channels = self.get_campaign_channels(campaign)
            if campaign_channels:
                scheduler = PostScheduler(self.db, self.bot, campaign_channels)
                self.schedulers[campaign] = scheduler
                self.components_status['schedulers'][campaign] = False
    
    def get_available_campaigns(self) -> List[str]:
        """Получение списка доступных кампаний"""
        campaigns = set()
        
        for channel_id, channel_data in ALL_CHANNELS.items():
            campaign = channel_data.get('campaign', 'default')
            campaigns.add(campaign)
        
        return list(campaigns)
    
    def get_campaign_channels(self, campaign: str) -> Dict:
        """Получение каналов для конкретной кампании"""
        campaign_channels = {}
        
        for channel_id, channel_data in ALL_CHANNELS.items():
            channel_campaign = channel_data.get('campaign', 'default')
            if channel_campaign == campaign:
                campaign_channels[channel_id] = channel_data
        
        return campaign_channels
    
    def register_handlers(self):
        """Регистрация обработчиков команд"""
        # Основные команды
        self.dp.message.register(self.start, Command(commands=["start"]))
        self.dp.message.register(self.help_command, Command(commands=["help"]))
        self.dp.message.register(self.campaigns, Command(commands=["campaigns"]))
        self.dp.message.register(self.status, Command(commands=["status"]))
        self.dp.message.register(self.generate_content, Command(commands=["generate"]))
        
        # Управление кампаниями
        self.dp.message.register(self.manage_campaign, Command(commands=["manage"]))
        self.dp.callback_query.register(self.handle_campaign_callback)
        
        # Управление постами
        self.dp.message.register(self.add_post, Command(commands=["add_post"]))
        self.dp.message.register(self.schedule_post, Command(commands=["schedule"]))
        self.dp.message.register(self.show_schedule, Command(commands=["schedule_list"]))
        
        # Аналитика
        self.dp.message.register(self.show_stats, Command(commands=["stats"]))
        self.dp.message.register(self.show_analytics, Command(commands=["analytics"]))
        
        # Управление системой
        self.dp.message.register(self.start_all, Command(commands=["start_all"]))
        self.dp.message.register(self.stop_all, Command(commands=["stop_all"]))
        self.dp.message.register(self.restart_all, Command(commands=["restart_all"]))
    
    async def start(self, message: types.Message):
        """Приветственное сообщение"""
        user = message.from_user
        if user.id != ADMIN_ID:
            await message.reply("❌ Этот бот предназначен только для администратора.")
            return

        welcome_text = f"""
🎯 Привет, {user.first_name}! 

Я универсальный бот для автопостинга с поддержкой множественных направлений.

📊 Доступные команды:
/campaigns - Управление кампаниями
/manage - Управление конкретной кампанией
/add_post - Добавить пост
/generate - Генерировать контент
/stats - Статистика
/status - Статус системы
/help - Помощь

🚀 Для начала работы используйте /campaigns
        """
        
        await message.reply(welcome_text)
    
    async def help_command(self, message: types.Message):
        """Справка по командам"""
        if message.from_user.id != ADMIN_ID:
            return

        help_text = """
📚 СПРАВКА ПО КОМАНДАМ

🎯 Управление кампаниями:
/campaigns - Просмотр всех кампаний
/manage - Управление конкретной кампанией

📝 Управление контентом:
/add_post - Добавить новый пост
/schedule - Запланировать пост
/schedule_list - Показать расписание
/generate - Генерировать контент

📊 Аналитика:
/stats - Общая статистика
/analytics - Детальная аналитика

⚙️ Управление системой:
/start_all - Запустить все компоненты
/stop_all - Остановить все компоненты
/restart_all - Перезапустить систему
/status - Статус компонентов

💡 Для получения помощи по конкретной команде используйте /help
        """
        await message.reply(help_text)
    
    async def campaigns(self, message: types.Message):
        """Показать все доступные кампании"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        campaigns_text = "🎯 ДОСТУПНЫЕ КАМПАНИИ\n\n"
        
        for campaign in campaigns:
            channels = self.get_campaign_channels(campaign)
            active_channels = [ch for ch in channels.values() if ch.get('active', True)]
            
            status = "🟢 Активна" if self.components_status['schedulers'].get(campaign, False) else "🔴 Неактивна"
            
            campaigns_text += f"📌 {campaign.upper()}\n"
            campaigns_text += f"   Статус: {status}\n"
            campaigns_text += f"   Каналов: {len(active_channels)}/{len(channels)}\n"
            campaigns_text += f"   Расписание: {len(POSTING_SCHEDULE.get(campaign, POSTING_SCHEDULE['default']))} дней\n"
            campaigns_text += "   " + "─" * 30 + "\n"
        
        # Создаем inline кнопки для управления
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔧 Управление", callback_data="manage_campaigns")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="campaign_stats")],
            [InlineKeyboardButton(text="🚀 Запустить все", callback_data="start_all_campaigns")]
        ])
        
        await message.reply(campaigns_text, reply_markup=keyboard)
    
    async def manage_campaign(self, message: types.Message):
        """Управление конкретной кампанией"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        # Создаем кнопки для каждой кампании
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=campaign.upper(), callback_data=f"manage_{campaign}")]
            for campaign in campaigns
        ])
        
        await message.reply("🎯 Выберите кампанию для управления:", reply_markup=keyboard)
    
    async def handle_campaign_callback(self, callback_query: types.CallbackQuery):
        """Обработка callback запросов"""
        if callback_query.from_user.id != ADMIN_ID:
            await callback_query.answer("❌ Доступ запрещен")
            return

        data = callback_query.data
        
        if data == "manage_campaigns":
            await self.manage_campaign(callback_query.message)
        
        elif data == "campaign_stats":
            await self.show_campaign_stats(callback_query.message)
        
        elif data == "start_all_campaigns":
            await self.start_all_campaigns(callback_query.message)
        
        elif data.startswith("manage_"):
            campaign = data.replace("manage_", "")
            await self.show_campaign_management(callback_query.message, campaign)
        
        elif data.startswith("campaign_"):
            parts = data.split("_")
            if len(parts) >= 3:
                campaign = parts[1]
                action = "_".join(parts[2:])
                await self.handle_campaign_action(callback_query.message, campaign, action)
        
        await callback_query.answer()
    
    async def show_campaign_management(self, message: types.Message, campaign: str):
        """Показать меню управления кампанией"""
        channels = self.get_campaign_channels(campaign)
        active_channels = [ch for ch in channels.values() if ch.get('active', True)]
        
        status = "🟢 Активна" if self.components_status['schedulers'].get(campaign, False) else "🔴 Неактивна"
        
        campaign_info = f"""
🎯 УПРАВЛЕНИЕ КАМПАНИЕЙ: {campaign.upper()}

📊 Статус: {status}
📢 Каналов: {len(active_channels)}/{len(channels)}
📅 Расписание: {len(POSTING_SCHEDULE.get(campaign, POSTING_SCHEDULE['default']))} дней
        """
        
        # Создаем кнопки управления
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="▶️ Запустить", callback_data=f"campaign_{campaign}_start"),
                InlineKeyboardButton(text="⏸️ Остановить", callback_data=f"campaign_{campaign}_stop")
            ],
            [
                InlineKeyboardButton(text="📝 Добавить пост", callback_data=f"campaign_{campaign}_add_post"),
                InlineKeyboardButton(text="📅 Расписание", callback_data=f"campaign_{campaign}_schedule")
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data=f"campaign_{campaign}_stats"),
                InlineKeyboardButton(text="⚙️ Настройки", callback_data=f"campaign_{campaign}_settings")
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="manage_campaigns")]
        ])
        
        await message.edit_text(campaign_info, reply_markup=keyboard)
    
    async def handle_campaign_action(self, message: types.Message, campaign: str, action: str):
        """Обработка действий с кампанией"""
        if action == "start":
            await self.start_campaign(message, campaign)
        elif action == "stop":
            await self.stop_campaign(message, campaign)
        elif action == "add_post":
            await self.add_post_to_campaign(message, campaign)
        elif action == "schedule":
            await self.show_campaign_schedule(message, campaign)
        elif action == "stats":
            await self.show_campaign_stats(message, campaign)
        elif action == "settings":
            await self.show_campaign_settings(message, campaign)
    
    async def start_campaign(self, message: types.Message, campaign: str):
        """Запуск кампании"""
        if campaign in self.schedulers:
            try:
                self.schedulers[campaign].start()
                self.components_status['schedulers'][campaign] = True
                await message.reply(f"✅ Кампания {campaign.upper()} запущена")
            except Exception as e:
                await message.reply(f"❌ Ошибка запуска кампании {campaign}: {e}")
        else:
            await message.reply(f"❌ Планировщик для кампании {campaign} не найден")
    
    async def stop_campaign(self, message: types.Message, campaign: str):
        """Остановка кампании"""
        if campaign in self.schedulers:
            try:
                self.schedulers[campaign].stop()
                self.components_status['schedulers'][campaign] = False
                await message.reply(f"⏸️ Кампания {campaign.upper()} остановлена")
            except Exception as e:
                await message.reply(f"❌ Ошибка остановки кампании {campaign}: {e}")
        else:
            await message.reply(f"❌ Планировщик для кампании {campaign} не найден")
    
    async def add_post_to_campaign(self, message: types.Message, campaign: str):
        """Добавление поста в кампанию"""
        channels = self.get_campaign_channels(campaign)
        active_channels = [ch for ch in channels.values() if ch.get('active', True)]
        
        if not active_channels:
            await message.reply(f"❌ Нет активных каналов в кампании {campaign}")
            return
        
        # Создаем кнопки для выбора канала
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=ch['name'], callback_data=f"channel_{ch['chat_id']}")]
            for ch in active_channels
        ])
        
        await message.reply(f"📢 Выберите канал для поста в кампании {campaign.upper()}:", reply_markup=keyboard)
    
    async def add_post(self, message: types.Message):
        """Добавить новый пост"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        # Создаем кнопки для выбора кампании
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=campaign.upper(), callback_data=f"add_post_{campaign}")]
            for campaign in campaigns
        ])
        
        await message.reply("🎯 Выберите кампанию для добавления поста:", reply_markup=keyboard)
    
    async def schedule_post(self, message: types.Message):
        """Запланировать пост"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        # Создаем кнопки для выбора кампании
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=campaign.upper(), callback_data=f"schedule_{campaign}")]
            for campaign in campaigns
        ])
        
        await message.reply("🎯 Выберите кампанию для планирования поста:", reply_markup=keyboard)
    
    async def show_schedule(self, message: types.Message):
        """Показать расписание постов"""
        if message.from_user.id != ADMIN_ID:
            return

        # Получаем запланированные посты из базы данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, c.name as channel_name 
            FROM posts p 
            LEFT JOIN channels c ON p.channel_id = c.chat_id
            WHERE p.published = FALSE 
            ORDER BY p.scheduled_time ASC
            LIMIT 20
        ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        if not posts:
            await message.reply("📅 Нет запланированных постов")
            return
        
        schedule_text = "📅 ЗАПЛАНИРОВАННЫЕ ПОСТЫ\n\n"
        
        for post in posts:
            scheduled_time = datetime.fromisoformat(post['scheduled_time'])
            schedule_text += f"🕐 {scheduled_time.strftime('%d.%m.%Y %H:%M')}\n"
            schedule_text += f"📢 {post['channel_name'] or post['channel_id']}\n"
            schedule_text += f"📝 {post['content'][:100]}...\n"
            schedule_text += "─" * 30 + "\n"
        
        await message.reply(schedule_text)
    
    async def show_analytics(self, message: types.Message):
        """Показать детальную аналитику"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        # Создаем кнопки для выбора кампании
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=campaign.upper(), callback_data=f"analytics_{campaign}")]
            for campaign in campaigns
        ])
        
        await message.reply("📊 Выберите кампанию для детальной аналитики:", reply_markup=keyboard)
    
    async def show_campaign_stats(self, message: types.Message):
        """Показать статистику кампаний"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        stats_text = "📊 СТАТИСТИКА КАМПАНИЙ\n\n"
        
        for campaign in campaigns:
            channels = self.get_campaign_channels(campaign)
            active_channels = [ch for ch in channels.values() if ch.get('active', True)]
            
            status = "🟢 Активна" if self.components_status['schedulers'].get(campaign, False) else "🔴 Неактивна"
            
            stats_text += f"📌 {campaign.upper()}\n"
            stats_text += f"   Статус: {status}\n"
            stats_text += f"   Каналов: {len(active_channels)}/{len(channels)}\n"
            stats_text += "   " + "─" * 30 + "\n"
        
        await message.reply(stats_text)
    
    async def show_campaign_schedule(self, message: types.Message, campaign: str):
        """Показать расписание кампании"""
        channels = self.get_campaign_channels(campaign)
        
        schedule_text = f"📅 РАСПИСАНИЕ КАМПАНИИ: {campaign.upper()}\n\n"
        
        for channel_id, channel_data in channels.items():
            schedule_text += f"📢 {channel_data['name']}\n"
            schedule_text += f"   ID: {channel_id}\n"
            schedule_text += f"   Статус: {'✅ Активен' if channel_data.get('active', True) else '❌ Неактивен'}\n"
            schedule_text += "   " + "─" * 20 + "\n"
        
        await message.reply(schedule_text)
    
    async def generate_content(self, message: types.Message):
        """Генерация контента"""
        if message.from_user.id != ADMIN_ID:
            return

        campaigns = self.get_available_campaigns()
        
        # Создаем кнопки для выбора кампании
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=campaign.upper(), callback_data=f"generate_{campaign}")]
            for campaign in campaigns
        ])
        
        await message.reply("🎯 Выберите кампанию для генерации контента:", reply_markup=keyboard)
    
    async def show_stats(self, message: types.Message):
        """Показать общую статистику"""
        if message.from_user.id != ADMIN_ID:
            return

        # Получаем статистику из базы данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Общая статистика
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE published = TRUE")
        published_posts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE error_message IS NOT NULL")
        failed_posts = cursor.fetchone()[0]
        
        # Статистика по кампаниям
        campaigns_stats = {}
        campaigns = self.get_available_campaigns()
        
        for campaign in campaigns:
            campaign_channels = self.get_campaign_channels(campaign)
            channel_ids = [ch['chat_id'] for ch in campaign_channels.values()]
            
            if channel_ids:
                placeholders = ','.join(['?' for _ in channel_ids])
                cursor.execute(f"SELECT COUNT(*) FROM posts WHERE channel_id IN ({placeholders})", channel_ids)
                campaign_posts = cursor.fetchone()[0]
                
                cursor.execute(f"SELECT COUNT(*) FROM posts WHERE channel_id IN ({placeholders}) AND published = TRUE", channel_ids)
                campaign_published = cursor.fetchone()[0]
                
                campaigns_stats[campaign] = {
                    'total': campaign_posts,
                    'published': campaign_published,
                    'success_rate': (campaign_published / campaign_posts * 100) if campaign_posts > 0 else 0
                }
        
        conn.close()
        
        # Формируем отчет
        stats_text = "📊 ОБЩАЯ СТАТИСТИКА\n\n"
        stats_text += f"📝 Всего постов: {total_posts}\n"
        stats_text += f"✅ Опубликовано: {published_posts}\n"
        stats_text += f"❌ Ошибок: {failed_posts}\n"
        stats_text += f"📈 Успешность: {(published_posts/total_posts*100 if total_posts > 0 else 0):.1f}%\n\n"
        
        stats_text += "🎯 ПО КАМПАНИЯМ:\n"
        for campaign, stats in campaigns_stats.items():
            status = "🟢" if self.components_status['schedulers'].get(campaign, False) else "🔴"
            stats_text += f"{status} {campaign.upper()}: {stats['published']}/{stats['total']} ({stats['success_rate']:.1f}%)\n"
        
        await message.reply(stats_text)
    
    async def status(self, message: types.Message):
        """Показать статус системы"""
        if message.from_user.id != ADMIN_ID:
            return

        status_text = "⚙️ СТАТУС СИСТЕМЫ\n\n"
        
        # Статус планировщиков
        status_text += "📅 ПЛАНИРОВЩИКИ:\n"
        for campaign, scheduler in self.schedulers.items():
            status = "🟢 Активен" if self.components_status['schedulers'].get(campaign, False) else "🔴 Неактивен"
            status_text += f"   {campaign.upper()}: {status}\n"
        
        # Статус генератора контента
        content_status = "🟢 Активен" if self.components_status['content_generator'] else "🔴 Неактивен"
        status_text += f"\n🤖 Генератор контента: {content_status}\n"
        
        # Создаем кнопки управления
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Запустить все", callback_data="start_all_campaigns"),
                InlineKeyboardButton(text="⏸️ Остановить все", callback_data="stop_all_campaigns")
            ],
            [InlineKeyboardButton(text="🔄 Перезапустить", callback_data="restart_all_campaigns")]
        ])
        
        await message.reply(status_text, reply_markup=keyboard)
    
    async def start_all(self, message: types.Message):
        """Запуск всех компонентов"""
        if message.from_user.id != ADMIN_ID:
            return

        await self.start_all_campaigns(message)
    
    async def start_all_campaigns(self, message: types.Message):
        """Запуск всех кампаний"""
        started_count = 0
        total_count = len(self.schedulers)
        
        for campaign, scheduler in self.schedulers.items():
            try:
                scheduler.start()
                self.components_status['schedulers'][campaign] = True
                started_count += 1
            except Exception as e:
                logger.error(f"Ошибка запуска кампании {campaign}: {e}")
        
        await message.reply(f"🚀 Запущено {started_count}/{total_count} кампаний")
    
    async def stop_all(self, message: types.Message):
        """Остановка всех компонентов"""
        if message.from_user.id != ADMIN_ID:
            return

        stopped_count = 0
        total_count = len(self.schedulers)
        
        for campaign, scheduler in self.schedulers.items():
            try:
                scheduler.stop()
                self.components_status['schedulers'][campaign] = False
                stopped_count += 1
            except Exception as e:
                logger.error(f"Ошибка остановки кампании {campaign}: {e}")
        
        await message.reply(f"⏸️ Остановлено {stopped_count}/{total_count} кампаний")
    
    async def restart_all(self, message: types.Message):
        """Перезапуск всех компонентов"""
        if message.from_user.id != ADMIN_ID:
            return

        await self.stop_all(message)
        await asyncio.sleep(2)
        await self.start_all(message)
    
    async def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск универсального бота...")
        
        # Запускаем планировщики
        for campaign, scheduler in self.schedulers.items():
            try:
                scheduler.start()
                self.components_status['schedulers'][campaign] = True
                logger.info(f"✅ Планировщик кампании {campaign} запущен")
            except Exception as e:
                logger.error(f"❌ Ошибка запуска планировщика {campaign}: {e}")
        
        # Запускаем бота
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    bot = UniversalBot()
    asyncio.run(bot.run()) 