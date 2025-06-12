import logging
import os
from datetime import datetime
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram import Update, ReplyKeyboardMarkup
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
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.scheduler = PostScheduler(self.db, self.application.bot, {})
        
        # Set up command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("add_post", self.add_post))
        self.application.add_handler(CommandHandler("schedule", self.show_schedule))
        self.application.add_handler(CommandHandler("stats", self.show_stats))
        self.application.add_handler(CommandHandler("channels", self.manage_channels))
        self.application.add_handler(CommandHandler("pause", self.pause_posting))
        self.application.add_handler(CommandHandler("resume", self.resume_posting))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        user = update.effective_user
        if user.id != ADMIN_ID:
            await update.message.reply_text("Sorry, this bot is for admin use only.")
            return

        await update.message.reply_text(
            f"Hi {user.first_name}! I'm your Telegram autoposting bot.\n\n"
            "Use /help to see available commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        if update.effective_user.id != ADMIN_ID:
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
        await update.message.reply_text(help_text)

    async def add_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start the process of adding a new post."""
        if update.effective_user.id != ADMIN_ID:
            return

        # Get available channels
        channels = self.db.get_active_channels()
        if not channels:
            await update.message.reply_text("No active channels found. Please add a channel first.")
            return

        # Create channel selection keyboard
        keyboard = [[channel['name']] for channel in channels]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            "Please select a channel for the post:",
            reply_markup=reply_markup
        )
        return CHOOSING_CHANNEL

    async def show_schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show the current posting schedule."""
        if update.effective_user.id != ADMIN_ID:
            return

        # Get pending posts
        pending_posts = self.db.get_pending_posts()
        
        if not pending_posts:
            await update.message.reply_text("No pending posts in the schedule.")
            return

        schedule_text = "📅 Pending Posts:\n\n"
        for post in pending_posts:
            schedule_text += f"ID: {post['id']}\n"
            schedule_text += f"Time: {post['scheduled_time']}\n"
            schedule_text += f"Channel: {post['channel_id']}\n"
            schedule_text += "---\n"

        await update.message.reply_text(schedule_text)

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show posting statistics."""
        if update.effective_user.id != ADMIN_ID:
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

        await update.message.reply_text(stats_text)

    async def pause_posting(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pause the autoposting scheduler."""
        if update.effective_user.id != ADMIN_ID:
            return

        self.scheduler.stop()
        await update.message.reply_text("Autoposting has been paused.")

    async def resume_posting(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Resume the autoposting scheduler."""
        if update.effective_user.id != ADMIN_ID:
            return

        self.scheduler.start()
        await update.message.reply_text("Autoposting has been resumed.")

    def run(self):
        """Start the bot."""
        # Start the scheduler
        self.scheduler.start()
        
        # Start the bot
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run() 