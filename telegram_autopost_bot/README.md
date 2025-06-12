# Telegram Autopost Bot

A Telegram bot for automated posting to channels with scheduling capabilities.

## Features

- Automated posting to multiple channels
- Post scheduling with customizable time slots
- Support for text, photo, and video posts
- Post templates for different content types
- Admin-only access
- Post statistics and monitoring
- Pause/Resume functionality

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd telegram_autopost_bot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here
MAIN_CHANNEL_ID=-100xxxxxxxxx
TEST_CHANNEL_ID=-100xxxxxxxxx
DATABASE_URL=data/posts.db
```

5. Get your bot token:
   - Message @BotFather on Telegram
   - Use the `/newbot` command
   - Follow the instructions to create your bot
   - Copy the API token provided

6. Get your Telegram ID:
   - Message @userinfobot on Telegram
   - It will reply with your ID

7. Get your channel ID:
   - Add @userinfobot to your channel
   - Forward a message from your channel to @userinfobot
   - It will reply with the channel ID

## Usage

1. Start the bot:
```bash
python main.py
```

2. Available commands:
- `/start` - Start the bot
- `/help` - Show help message
- `/add_post` - Add a new post
- `/schedule` - Show posting schedule
- `/stats` - Show posting statistics
- `/channels` - Manage channels
- `/pause` - Pause autoposting
- `/resume` - Resume autoposting

## Project Structure

```
telegram_autopost_bot/
├── main.py                 # Main bot file
├── config.py              # Configuration settings
├── database.py            # Database operations
├── scheduler.py           # Post scheduling
├── requirements.txt       # Python dependencies
└── data/                  # Data directory
    └── posts.db          # SQLite database
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 