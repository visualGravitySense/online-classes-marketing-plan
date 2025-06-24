#!/usr/bin/env python3
"""
Модуль интеграции для подключения фронтенда к универсальному боту
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Добавляем путь к модулям
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from config import ALL_CHANNELS, POSTING_SCHEDULE, POST_TEMPLATES
    from database import Database
    from integrated_content_generator import ContentGenerator
except ImportError as e:
    print(f"Предупреждение: Не удалось импортировать модули бота: {e}")
    # Создаем заглушки для тестового режима
    ALL_CHANNELS = {}
    POSTING_SCHEDULE = {'default': {}}
    POST_TEMPLATES = {'default': {}}
    
    class Database:
        def __init__(self, db_path):
            self.db_path = db_path
        
        def get_connection(self):
            return None
        
        def add_post(self, *args, **kwargs):
            return 1
        
        def delete_post(self, *args, **kwargs):
            pass
    
    class ContentGenerator:
        def generate_post(self, *args, **kwargs):
            return "Тестовый контент"

@dataclass
class BotCampaign:
    """Модель кампании для фронтенда"""
    id: str
    name: str
    description: str
    status: str
    channels: List[Dict]
    posts_count: int
    scheduled_posts: int
    created_at: str
    updated_at: str

@dataclass
class BotChannel:
    """Модель канала для фронтенда"""
    id: str
    name: str
    chat_id: str
    campaign: str
    status: str
    posts_count: int
    last_post_date: Optional[str]

@dataclass
class BotPost:
    """Модель поста для фронтенда"""
    id: str
    content: str
    media_urls: Optional[List[str]]
    campaign: str
    channels: List[str]
    status: str
    scheduled_time: Optional[str]
    published_time: Optional[str]
    created_at: str
    updated_at: str

@dataclass
class BotAnalytics:
    """Модель аналитики для фронтенда"""
    campaigns: Dict[str, int]
    posts: Dict[str, int]
    channels: Dict[str, int]
    engagement: Dict[str, Any]
    performance: Dict[str, Any]

@dataclass
class BotSystemStatus:
    """Модель статуса системы для фронтенда"""
    schedulers: Dict[str, Dict]
    content_generator: Dict[str, Any]
    database: Dict[str, Any]
    telegram_api: Dict[str, Any]

class BotIntegration:
    """Класс для интеграции фронтенда с универсальным ботом"""
    
    def __init__(self):
        self.db = Database('data/posts.db')
        self.content_generator = ContentGenerator()
        
        # Инициализируем планировщики для каждой кампании
        self.schedulers = {}
        self.initialize_schedulers()
        
        # Статус компонентов
        self.components_status = {
            'schedulers': {},
            'content_generator': False,
            'database': {'status': 'connected'},
            'telegram_api': {'status': 'connected'}
        }
    
    def initialize_schedulers(self):
        """Инициализация планировщиков для каждой кампании"""
        campaigns = self.get_available_campaigns()
        
        for campaign in campaigns:
            campaign_channels = self.get_campaign_channels(campaign)
            if campaign_channels:
                # Создаем планировщик только если есть каналы
                self.components_status['schedulers'][campaign] = {
                    'status': 'stopped',
                    'last_run': None,
                    'next_run': None,
                    'error_message': None
                }
    
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
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Получение данных для дашборда"""
        campaigns = self.get_available_campaigns()
        
        # Подсчитываем статистику
        total_campaigns = len(campaigns)
        active_campaigns = sum(1 for campaign in campaigns 
                             if self.components_status['schedulers'].get(campaign, {}).get('status') == 'running')
        
        # Получаем статистику по постам
        posts_stats = self.get_posts_statistics()
        
        # Получаем статистику по каналам
        channels_stats = self.get_channels_statistics()
        
        # Получаем статистику вовлеченности (пока тестовые данные)
        engagement_stats = {
            'average_engagement_rate': 4.2,
            'total_views': 15420,
            'total_likes': 648,
            'total_shares': 234
        }
        
        return {
            'campaigns': {
                'total': total_campaigns,
                'active': active_campaigns,
                'inactive': total_campaigns - active_campaigns
            },
            'posts': posts_stats,
            'channels': channels_stats,
            'engagement': engagement_stats
        }
    
    def get_campaigns_data(self) -> List[BotCampaign]:
        """Получение данных о кампаниях"""
        campaigns = []
        
        for campaign_name in self.get_available_campaigns():
            channels = self.get_campaign_channels(campaign_name)
            active_channels = [ch for ch in channels.values() if ch.get('active', True)]
            
            # Получаем количество постов для кампании
            posts_count = self.get_campaign_posts_count(campaign_name)
            scheduled_posts = self.get_campaign_scheduled_posts_count(campaign_name)
            
            # Определяем статус кампании
            scheduler_status = self.components_status['schedulers'].get(campaign_name, {})
            status = 'active' if scheduler_status.get('status') == 'running' else 'inactive'
            
            # Формируем список каналов для фронтенда
            channels_list = []
            for channel_id, channel_data in channels.items():
                channels_list.append({
                    'id': channel_id,
                    'name': channel_data.get('name', channel_id),
                    'chat_id': channel_data.get('chat_id', ''),
                    'status': 'active' if channel_data.get('active', True) else 'inactive'
                })
            
            campaign = BotCampaign(
                id=campaign_name,
                name=campaign_name.upper(),
                description=self.get_campaign_description(campaign_name),
                status=status,
                channels=channels_list,
                posts_count=posts_count,
                scheduled_posts=scheduled_posts,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            campaigns.append(campaign)
        
        return campaigns
    
    def get_channels_data(self) -> List[BotChannel]:
        """Получение данных о каналах"""
        channels = []
        
        for channel_id, channel_data in ALL_CHANNELS.items():
            campaign = channel_data.get('campaign', 'default')
            posts_count = self.get_channel_posts_count(channel_id)
            last_post_date = self.get_channel_last_post_date(channel_id)
            
            channel = BotChannel(
                id=channel_id,
                name=channel_data.get('name', channel_id),
                chat_id=channel_data.get('chat_id', ''),
                campaign=campaign,
                status='active' if channel_data.get('active', True) else 'inactive',
                posts_count=posts_count,
                last_post_date=last_post_date
            )
            
            channels.append(channel)
        
        return channels
    
    def get_posts_data(self) -> List[BotPost]:
        """Получение данных о постах"""
        # Получаем посты из базы данных
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, content, media_path, channel_id, scheduled_time, published, created_at
            FROM posts
            ORDER BY created_at DESC
            LIMIT 100
        ''')
        
        posts = []
        for row in cursor.fetchall():
            post_id, content, media_path, channel_id, scheduled_time, published, created_at = row
            
            # Определяем кампанию по каналу
            campaign = self.get_channel_campaign(channel_id)
            
            # Определяем статус
            if published:
                status = 'published'
            elif scheduled_time and datetime.fromisoformat(scheduled_time) > datetime.now():
                status = 'scheduled'
            else:
                status = 'draft'
            
            # Формируем media_urls
            media_urls = [media_path] if media_path else None
            
            post = BotPost(
                id=str(post_id),
                content=content,
                media_urls=media_urls,
                campaign=campaign,
                channels=[channel_id],
                status=status,
                scheduled_time=scheduled_time,
                published_time=created_at if published else None,
                created_at=created_at,
                updated_at=created_at
            )
            
            posts.append(post)
        
        conn.close()
        return posts
    
    def create_campaign(self, name: str, description: str = "", channels: List[str] = None) -> BotCampaign:
        """Создание новой кампании"""
        # В текущей реализации кампании определяются конфигурацией
        # Здесь можно добавить логику для создания пользовательских кампаний
        
        campaign = BotCampaign(
            id=f"custom-{int(time.time())}",
            name=name,
            description=description,
            status='inactive',
            channels=[],
            posts_count=0,
            scheduled_posts=0,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        return campaign
    
    def start_campaign(self, campaign_id: str) -> bool:
        """Запуск кампании"""
        try:
            if campaign_id in self.components_status['schedulers']:
                self.components_status['schedulers'][campaign_id] = {
                    'status': 'running',
                    'last_run': datetime.now().isoformat(),
                    'next_run': (datetime.now() + timedelta(hours=1)).isoformat(),
                    'error_message': None
                }
                return True
            return False
        except Exception as e:
            if campaign_id in self.components_status['schedulers']:
                self.components_status['schedulers'][campaign_id]['error_message'] = str(e)
            return False
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Приостановка кампании"""
        try:
            if campaign_id in self.components_status['schedulers']:
                self.components_status['schedulers'][campaign_id] = {
                    'status': 'stopped',
                    'last_run': datetime.now().isoformat(),
                    'next_run': None,
                    'error_message': None
                }
                return True
            return False
        except Exception as e:
            if campaign_id in self.components_status['schedulers']:
                self.components_status['schedulers'][campaign_id]['error_message'] = str(e)
            return False
    
    def delete_campaign(self, campaign_id: str) -> bool:
        """Удаление кампании"""
        try:
            if campaign_id in self.components_status['schedulers']:
                del self.components_status['schedulers'][campaign_id]
                return True
            return False
        except Exception:
            return False
    
    def create_post(self, content: str, campaign: str, channels: List[str], scheduled_time: str = None) -> BotPost:
        """Создание нового поста"""
        try:
            # Добавляем пост в базу данных
            scheduled_datetime = datetime.fromisoformat(scheduled_time) if scheduled_time else datetime.now()
            
            # Для каждого канала создаем отдельную запись
            for channel_id in channels:
                self.db.add_post(
                    content=content,
                    channel_id=channel_id,
                    scheduled_time=scheduled_datetime
                )
            
            post = BotPost(
                id=f"post-{int(time.time())}",
                content=content,
                media_urls=None,
                campaign=campaign,
                channels=channels,
                status='draft' if not scheduled_time else 'scheduled',
                scheduled_time=scheduled_time,
                published_time=None,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            return post
        except Exception as e:
            raise Exception(f"Ошибка создания поста: {str(e)}")
    
    def delete_post(self, post_id: str) -> bool:
        """Удаление поста"""
        try:
            self.db.delete_post(int(post_id))
            return True
        except Exception:
            return False
    
    def generate_content(self, topic: str, campaign: str, tone: str, length: str, 
                        target_audience: str, platform: str, include_hashtags: bool = True,
                        include_call_to_action: bool = True) -> Dict[str, Any]:
        """Генерация контента"""
        try:
            # Используем существующий генератор контента
            generated_content = self.content_generator.generate_post(
                topic=topic,
                tone=tone,
                length=length,
                platform=platform,
                target_audience=target_audience
            )
            
            # Добавляем хештеги если нужно
            hashtags = []
            if include_hashtags:
                hashtags = self.generate_hashtags(topic, campaign)
            
            # Добавляем призыв к действию если нужно
            call_to_action = ""
            if include_call_to_action:
                call_to_action = self.generate_call_to_action(platform)
            
            return {
                'content': generated_content,
                'hashtags': hashtags,
                'call_to_action': call_to_action,
                'campaign': campaign,
                'platform': platform,
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
        except Exception as e:
            raise Exception(f"Ошибка генерации контента: {str(e)}")
    
    def get_system_status(self) -> BotSystemStatus:
        """Получение статуса системы"""
        return BotSystemStatus(
            schedulers=self.components_status['schedulers'],
            content_generator={
                'status': 'available' if self.content_generator else 'unavailable',
                'last_generation': datetime.now().isoformat(),
                'error_message': None
            },
            database={
                'status': 'connected',
                'last_backup': datetime.now().isoformat()
            },
            telegram_api={
                'status': 'connected',
                'last_check': datetime.now().isoformat()
            }
        )
    
    # Вспомогательные методы
    
    def get_campaign_description(self, campaign: str) -> str:
        """Получение описания кампании"""
        descriptions = {
            'default': 'Кампания для продвижения курсов по UX/UI дизайну',
            'digitalizacija': 'Кампания для продвижения услуг цифровизации бизнеса'
        }
        return descriptions.get(campaign, f'Кампания {campaign}')
    
    def get_posts_statistics(self) -> Dict[str, int]:
        """Получение статистики по постам"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Общее количество постов
        cursor.execute('SELECT COUNT(*) FROM posts')
        total = cursor.fetchone()[0]
        
        # Опубликованные посты
        cursor.execute('SELECT COUNT(*) FROM posts WHERE published = TRUE')
        published = cursor.fetchone()[0]
        
        # Запланированные посты
        cursor.execute('''
            SELECT COUNT(*) FROM posts 
            WHERE published = FALSE AND scheduled_time > datetime('now')
        ''')
        scheduled = cursor.fetchone()[0]
        
        # Посты с ошибками
        cursor.execute('SELECT COUNT(*) FROM posts WHERE error_message IS NOT NULL')
        failed = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'published': published,
            'scheduled': scheduled,
            'failed': failed
        }
    
    def get_channels_statistics(self) -> Dict[str, int]:
        """Получение статистики по каналам"""
        total = len(ALL_CHANNELS)
        active = sum(1 for ch in ALL_CHANNELS.values() if ch.get('active', True))
        
        return {
            'total': total,
            'active': active,
            'inactive': total - active
        }
    
    def get_campaign_posts_count(self, campaign: str) -> int:
        """Получение количества постов для кампании"""
        campaign_channels = self.get_campaign_channels(campaign)
        channel_ids = list(campaign_channels.keys())
        
        if not channel_ids:
            return 0
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in channel_ids])
        cursor.execute(f'SELECT COUNT(*) FROM posts WHERE channel_id IN ({placeholders})', channel_ids)
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_campaign_scheduled_posts_count(self, campaign: str) -> int:
        """Получение количества запланированных постов для кампании"""
        campaign_channels = self.get_campaign_channels(campaign)
        channel_ids = list(campaign_channels.keys())
        
        if not channel_ids:
            return 0
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in channel_ids])
        cursor.execute(f'''
            SELECT COUNT(*) FROM posts 
            WHERE channel_id IN ({placeholders}) 
            AND published = FALSE 
            AND scheduled_time > datetime('now')
        ''', channel_ids)
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_channel_posts_count(self, channel_id: str) -> int:
        """Получение количества постов для канала"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM posts WHERE channel_id = ?', (channel_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_channel_last_post_date(self, channel_id: str) -> Optional[str]:
        """Получение даты последнего поста для канала"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT created_at FROM posts 
            WHERE channel_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (channel_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_channel_campaign(self, channel_id: str) -> str:
        """Получение кампании по ID канала"""
        channel_data = ALL_CHANNELS.get(channel_id, {})
        return channel_data.get('campaign', 'default')
    
    def generate_hashtags(self, topic: str, campaign: str) -> List[str]:
        """Генерация хештегов"""
        if 'дизайн' in topic.lower() or 'ux' in topic.lower() or 'ui' in topic.lower():
            return ['#дизайн', '#UX', '#UI', '#образование', '#интерфейс']
        elif 'бизнес' in topic.lower() or 'цифровизация' in topic.lower():
            return ['#бизнес', '#цифровизация', '#автоматизация', '#эффективность']
        else:
            return ['#полезное', '#интересное', '#образование']
    
    def generate_call_to_action(self, platform: str) -> str:
        """Генерация призыва к действию"""
        cta_templates = {
            'telegram': 'Подписывайтесь на наш канал для получения полезных материалов!',
            'instagram': 'Подписывайтесь на наш аккаунт для ежедневных советов!',
            'facebook': 'Присоединяйтесь к нашему сообществу!',
            'linkedin': 'Подключайтесь к нашей сети профессионалов!'
        }
        return cta_templates.get(platform, 'Следите за нашими обновлениями!')

# Создаем глобальный экземпляр интеграции
bot_integration = BotIntegration() 