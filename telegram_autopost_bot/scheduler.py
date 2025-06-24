import schedule
import time
import threading
import asyncio
from datetime import datetime
import pytz
from typing import Callable, Dict, List
import logging
from aiogram import Bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self, db, bot: Bot, posting_schedule: Dict[str, List[str]]):
        self.db = db
        self.bot = bot
        self.posting_schedule = posting_schedule
        self.running = False
        self.scheduler_thread = None
        self.loop = None

    def start(self):
        """Start the scheduler in a separate thread."""
        if self.running:
            return
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler_thread)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Scheduler started in separate thread")

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def _run_scheduler_thread(self):
        """Run scheduler in a separate thread."""
        # Create new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Schedule the periodic task
        schedule.every(1).minutes.do(self._check_and_publish_posts)
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in scheduler thread: {str(e)}")
                time.sleep(60)

    def _check_and_publish_posts(self):
        """Check for pending posts and publish them."""
        try:
            # Создаем задачу в event loop
            task = self.loop.create_task(self._process_pending_posts())
            # Ждем завершения задачи
            self.loop.run_until_complete(task)
        except Exception as e:
            logger.error(f"Error checking posts: {str(e)}")

    async def _process_pending_posts(self):
        """Process all pending posts that are due for publishing."""
        try:
            pending_posts = self.db.get_pending_posts()
            logger.info(f"Found {len(pending_posts)} pending posts")
            
            for post in pending_posts:
                try:
                    await self._publish_post(post)
                    # Small delay between posts to avoid rate limiting
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"Error publishing post {post['id']}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error processing pending posts: {str(e)}")

    async def _publish_post(self, post: dict):
        """Publish a post to the specified channel."""
        try:
            channel_id = post['channel_id']
            content = post['content']
            
            logger.info(f"Publishing post {post['id']} to {channel_id}")
            
            # Добавляем timeout для API вызовов
            timeout = 30  # 30 секунд
            
            # Handle media if present
            if post['media_path'] and post['media_type']:
                if post['media_type'] == 'photo':
                    await asyncio.wait_for(
                        self.bot.send_photo(
                            chat_id=channel_id,
                            photo=open(post['media_path'], 'rb'),
                            caption=content
                        ),
                        timeout=timeout
                    )
                elif post['media_type'] == 'video':
                    await asyncio.wait_for(
                        self.bot.send_video(
                            chat_id=channel_id,
                            video=open(post['media_path'], 'rb'),
                            caption=content
                        ),
                        timeout=timeout
                    )
            else:
                await asyncio.wait_for(
                    self.bot.send_message(
                        chat_id=channel_id,
                        text=content
                    ),
                    timeout=timeout
                )
            
            # Mark post as published
            self.db.mark_post_published(post['id'])
            logger.info(f"Successfully published post {post['id']} to {channel_id}")
            
        except asyncio.TimeoutError:
            error_msg = f"Timeout publishing post {post['id']} to {channel_id}"
            logger.error(error_msg)
            self.db.mark_post_published(post['id'], error_msg)
        except Exception as e:
            error_msg = f"Failed to publish post {post['id']}: {str(e)}"
            logger.error(error_msg)
            self.db.mark_post_published(post['id'], error_msg)

    def schedule_post(self, post_id: int, scheduled_time: datetime):
        """Schedule a post for publishing at a specific time."""
        try:
            # Convert to local timezone if needed
            local_tz = pytz.timezone('UTC')  # Change this to your desired timezone
            if scheduled_time.tzinfo is None:
                scheduled_time = local_tz.localize(scheduled_time)
            
            # Schedule the post
            schedule.every().day.at(scheduled_time.strftime('%H:%M')).do(
                lambda: self._check_and_publish_posts()
            )
            
            logger.info(f"Scheduled post {post_id} for {scheduled_time}")
        except Exception as e:
            logger.error(f"Error scheduling post {post_id}: {str(e)}") 