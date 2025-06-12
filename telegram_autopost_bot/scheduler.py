import schedule
import time
import threading
from datetime import datetime
import pytz
from typing import Callable, Dict, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self, db, bot, posting_schedule: Dict[str, List[str]]):
        self.db = db
        self.bot = bot
        self.posting_schedule = posting_schedule
        self.running = False
        self.scheduler_thread = None

    def start(self):
        """Start the scheduler in a separate thread."""
        if self.running:
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("Scheduler stopped")

    def _run_scheduler(self):
        """Main scheduler loop."""
        while self.running:
            try:
                # Check for pending posts
                self._process_pending_posts()
                
                # Run scheduled tasks
                schedule.run_pending()
                
                # Sleep for a minute
                time.sleep(60)
            except Exception as e:
                logger.error(f"Error in scheduler: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying

    def _process_pending_posts(self):
        """Process all pending posts that are due for publishing."""
        try:
            pending_posts = self.db.get_pending_posts()
            for post in pending_posts:
                self._publish_post(post)
        except Exception as e:
            logger.error(f"Error processing pending posts: {str(e)}")

    async def _publish_post(self, post: dict):
        """Publish a post to the specified channel."""
        try:
            channel_id = post['channel_id']
            content = post['content']
            
            # Handle media if present
            if post['media_path'] and post['media_type']:
                if post['media_type'] == 'photo':
                    await self.bot.send_photo(
                        chat_id=channel_id,
                        photo=open(post['media_path'], 'rb'),
                        caption=content
                    )
                elif post['media_type'] == 'video':
                    await self.bot.send_video(
                        chat_id=channel_id,
                        video=open(post['media_path'], 'rb'),
                        caption=content
                    )
            else:
                await self.bot.send_message(
                    chat_id=channel_id,
                    text=content
                )
            
            # Mark post as published
            self.db.mark_post_published(post['id'])
            logger.info(f"Successfully published post {post['id']}")
            
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
                self._process_pending_posts
            )
            
            logger.info(f"Scheduled post {post_id} for {scheduled_time}")
        except Exception as e:
            logger.error(f"Error scheduling post {post_id}: {str(e)}") 