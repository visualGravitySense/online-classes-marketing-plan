import sqlite3
from datetime import datetime
import os
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self) -> None:
        """Initialize the database with required tables."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                media_path TEXT,
                media_type TEXT,
                channel_id TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                published BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT
            )
        ''')
        
        # Channels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                chat_id TEXT UNIQUE NOT NULL,
                active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def add_post(self, content: str, channel_id: str, scheduled_time: datetime,
                media_path: Optional[str] = None, media_type: Optional[str] = None) -> int:
        """Add a new post to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (content, media_path, media_type, channel_id, scheduled_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (content, media_path, media_type, channel_id, scheduled_time))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return post_id

    def get_pending_posts(self) -> List[Dict[str, Any]]:
        """Get all pending posts that are due for publishing."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM posts 
            WHERE published = FALSE 
            AND scheduled_time <= datetime('now')
            ORDER BY scheduled_time ASC
        ''')
        
        columns = [description[0] for description in cursor.description]
        posts = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return posts

    def mark_post_published(self, post_id: int, error_message: Optional[str] = None) -> None:
        """Mark a post as published or failed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if error_message:
            cursor.execute('''
                UPDATE posts 
                SET published = TRUE, error_message = ?
                WHERE id = ?
            ''', (error_message, post_id))
        else:
            cursor.execute('''
                UPDATE posts 
                SET published = TRUE
                WHERE id = ?
            ''', (post_id,))
        
        conn.commit()
        conn.close()

    def add_channel(self, name: str, chat_id: str) -> None:
        """Add a new channel to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO channels (name, chat_id)
            VALUES (?, ?)
        ''', (name, chat_id))
        
        conn.commit()
        conn.close()

    def get_active_channels(self) -> List[Dict[str, Any]]:
        """Get all active channels."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM channels WHERE active = TRUE')
        
        columns = [description[0] for description in cursor.description]
        channels = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return channels

    def delete_post(self, post_id: int) -> None:
        """Delete a post by its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()

    def update_post(self, post_id: int, content: str, channel_id: str, scheduled_time: datetime, media_path: Optional[str] = None, media_type: Optional[str] = None) -> None:
        """Update an existing post by its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE posts
            SET content = ?, channel_id = ?, scheduled_time = ?, media_path = ?, media_type = ?
            WHERE id = ?
        ''', (content, channel_id, scheduled_time, media_path, media_type, post_id))
        conn.commit()
        conn.close() 