import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, ADMIN_ID, CHANNELS, POST_TEMPLATES
from database import Database
from scheduler import PostScheduler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
CHOOSING_CHANNEL, ENTERING_CONTENT, ENTERING_MEDIA, ENTERING_TIME = range(4)

class TelegramBot:
    def __init__(self):
        self.db = Database('data/posts.db')
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.scheduler = PostScheduler(self.db, self.bot, {})
        
        # Set up command handlers
        self.dp.message.register(self.start, Command(commands=["start"]))
        self.dp.message.register(self.help_command, Command(commands=["help"]))
        self.dp.message.register(self.add_post, Command(commands=["add_post"]))
        self.dp.message.register(self.show_schedule, Command(commands=["schedule"]))
        self.dp.message.register(self.show_stats, Command(commands=["stats"]))
        self.dp.message.register(self.manage_channels, Command(commands=["channels"]))
        self.dp.message.register(self.pause_posting, Command(commands=["pause"]))
        self.dp.message.register(self.resume_posting, Command(commands=["resume"]))

    async def start(self, message: types.Message):
        """Send a message when the command /start is issued."""
        user = message.from_user
        if user.id != ADMIN_ID:
            await message.reply("Sorry, this bot is for admin use only.")
            return

        await message.reply(
            f"Hi {user.first_name}! I'm your Telegram autoposting bot.\n\n"
            "Use /help to see available commands."
        )

    async def help_command(self, message: types.Message):
        """Send a message when the command /help is issued."""
        if message.from_user.id != ADMIN_ID:
            return

        help_text = """
Available commands:
/add_post - Add a new post
/schedule - Show posting schedule
/stats - Show posting statistics
/channels - Manage channels
/pause - Pause autoposting
/resume - Resume autoposting
/help - Show this help message
"""
        await message.reply(help_text)

    async def add_post(self, message: types.Message):
        """Start the process of adding a new post."""
        if message.from_user.id != ADMIN_ID:
            return

        # Get available channels
        channels = self.db.get_active_channels()
        if not channels:
            await message.reply("No active channels found. Please add a channel first.")
            return

        # Create channel selection keyboard
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=channel['name'])] for channel in channels],
            one_time_keyboard=True
        )

        await message.reply(
            "Please select a channel for the post:",
            reply_markup=keyboard
        )

    async def show_schedule(self, message: types.Message):
        """Show the current posting schedule."""
        if message.from_user.id != ADMIN_ID:
            return

        # Get pending posts
        pending_posts = self.db.get_pending_posts()
        
        if not pending_posts:
            await message.reply("No pending posts in the schedule.")
            return

        schedule_text = "📅 Pending Posts:\n\n"
        for post in pending_posts:
            schedule_text += f"ID: {post['id']}\n"
            schedule_text += f"Time: {post['scheduled_time']}\n"
            schedule_text += f"Channel: {post['channel_id']}\n"
            schedule_text += "---\n"

        await message.reply(schedule_text)

    async def show_stats(self, message: types.Message):
        """Show posting statistics."""
        if message.from_user.id != ADMIN_ID:
            return

        # Get statistics from database
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Total posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        
        # Published posts
        cursor.execute("SELECT COUNT(*) FROM posts WHERE published = TRUE")
        published_posts = cursor.fetchone()[0]
        
        # Failed posts
        cursor.execute("SELECT COUNT(*) FROM posts WHERE error_message IS NOT NULL")
        failed_posts = cursor.fetchone()[0]
        
        conn.close()

        stats_text = "📊 Posting Statistics:\n\n"
        stats_text += f"Total Posts: {total_posts}\n"
        stats_text += f"Published: {published_posts}\n"
        stats_text += f"Failed: {failed_posts}\n"
        stats_text += f"Success Rate: {(published_posts/total_posts*100 if total_posts > 0 else 0):.1f}%"

        await message.reply(stats_text)

    async def manage_channels(self, message: types.Message):
        """Manage channels for posting."""
        if message.from_user.id != ADMIN_ID:
            return

        # Get all channels
        channels = self.db.get_active_channels()
        
        if not channels:
            await message.reply("No channels configured. Use /add_channel to add a new channel.")
            return

        channels_text = "📢 Configured Channels:\n\n"
        for channel in channels:
            status = "✅ Active" if channel['active'] else "❌ Inactive"
            channels_text += f"Name: {channel['name']}\n"
            channels_text += f"ID: {channel['chat_id']}\n"
            channels_text += f"Status: {status}\n"
            channels_text += "---\n"

        await message.reply(channels_text)

    async def pause_posting(self, message: types.Message):
        """Pause the autoposting scheduler."""
        if message.from_user.id != ADMIN_ID:
            return

        await self.scheduler.stop()
        await message.reply("Autoposting has been paused.")

    async def resume_posting(self, message: types.Message):
        """Resume the autoposting scheduler."""
        if message.from_user.id != ADMIN_ID:
            return

        await self.scheduler.start()
        await message.reply("Autoposting has been resumed.")

    async def run(self):
        """Start the bot."""
        # Start the scheduler
        await self.scheduler.start()
        
        # Start the bot
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    import asyncio
    bot = TelegramBot()
    asyncio.run(bot.run()) 