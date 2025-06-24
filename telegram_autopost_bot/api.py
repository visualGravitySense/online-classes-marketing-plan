from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
import json
import os
from pathlib import Path as PathLib
from aiogram import Bot

from database import Database
from scheduler import PostScheduler
from config import BOT_TOKEN, ADMIN_ID


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
templates_path = PathLib(__file__).parent.parent / "templates"
if templates_path.exists():
    app.mount("/templates", StaticFiles(directory=str(templates_path)), name="templates")

# Initialize bot and database
bot = Bot(token=BOT_TOKEN)
db = Database('data/posts.db')
scheduler = PostScheduler(db, bot, {})

# Main page
@app.get("/")
async def main_page():
    """Serve the main dashboard"""
    dashboard_path = PathLib(__file__).parent.parent / "templates" / "dashboard_hub.html"
    if dashboard_path.exists():
        return FileResponse(str(dashboard_path))
    else:
        return {"message": "Dashboard not found. Please check templates/dashboard_hub.html"}

# Models
class Post(BaseModel):
    content: str
    channel_id: str
    scheduled_time: datetime
    media_path: Optional[str] = None
    media_type: Optional[str] = None

class Channel(BaseModel):
    name: str
    chat_id: str
    active: bool = True

class TestPostRequest(BaseModel):
    channel_id: str
    content: Optional[str] = 'Тестовый пост!'

class ContentGenerationRequest(BaseModel):
    audience_group: str
    content_type: str
    channel_id: str
    scheduled_time: Optional[datetime] = None
    custom_prompt: Optional[str] = None

class ContentPreview(BaseModel):
    content: str
    audience_group: str
    content_type: str
    preview_id: str

# API Endpoints
@app.get("/api/status")
async def get_status():
    """Get API status"""
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/stats")
async def get_stats():
    """Get posting statistics"""
    conn = db.get_connection()
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
    
    # Active channels
    cursor.execute("SELECT COUNT(*) FROM channels WHERE active = TRUE")
    active_channels = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "failed_posts": failed_posts,
        "active_channels": active_channels,
        "success_rate": (published_posts/total_posts*100 if total_posts > 0 else 0)
    }

@app.get("/api/channels")
async def get_channels():
    """Get all channels"""
    return db.get_active_channels()

@app.post("/api/channels")
async def add_channel(channel: Channel):
    """Add a new channel"""
    try:
        db.add_channel(channel.name, channel.chat_id)
        return {"status": "success", "message": "Channel added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/posts")
async def get_posts():
    """Get all posts"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name as channel_name 
        FROM posts p 
        LEFT JOIN channels c ON p.channel_id = c.chat_id 
        ORDER BY p.scheduled_time DESC
    """)
    
    columns = [description[0] for description in cursor.description]
    posts = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    # Преобразуем scheduled_time в ISO-формат с 'T'
    for post in posts:
        st = post.get('scheduled_time')
        if st and isinstance(st, str) and ' ' in st:
            # Преобразуем '2025-06-13 10:25:00+00:00' -> '2025-06-13T10:25:00+00:00'
            post['scheduled_time'] = st.replace(' ', 'T', 1)
    return posts

@app.post("/api/posts")
async def create_post(post: Post):
    """Create a new post"""
    try:
        post_id = db.add_post(
            content=post.content,
            channel_id=post.channel_id,
            scheduled_time=post.scheduled_time,
            media_path=post.media_path,
            media_type=post.media_type
        )
        return {"status": "success", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/activity")
async def get_activity():
    """Get recent activity"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name as channel_name 
        FROM posts p 
        LEFT JOIN channels c ON p.channel_id = c.chat_id 
        WHERE p.published = TRUE 
        ORDER BY p.scheduled_time DESC 
        LIMIT 10
    """)
    
    columns = [description[0] for description in cursor.description]
    activities = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return activities

@app.post("/api/scheduler/start")
async def start_scheduler():
    """Start the scheduler"""
    try:
        scheduler.start()
        return {"status": "success", "message": "Scheduler started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scheduler/stop")
async def stop_scheduler():
    """Stop the scheduler"""
    try:
        scheduler.stop()
        return {"status": "success", "message": "Scheduler stopped"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int = Path(..., description="ID поста для удаления")):
    try:
        db.delete_post(post_id)
        return {"status": "success", "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    try:
        db.update_post(
            post_id=post_id,
            content=post.content,
            channel_id=post.channel_id,
            scheduled_time=post.scheduled_time,
            media_path=post.media_path,
            media_type=post.media_type
        )
        return {"status": "success", "message": "Post updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/test_post")
async def send_test_post(req: TestPostRequest):
    """Send a test post to a channel immediately."""
    try:
        await bot.send_message(chat_id=req.channel_id, text=req.content or 'Тестовый пост!')
        return {"status": "success", "message": "Test post sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/channels/{chat_id}")
async def delete_channel(chat_id: str):
    try:
        db.delete_channel(chat_id)
        return {"status": "success", "message": "Channel deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/channels")
async def delete_all_channels():
    try:
        db.delete_all_channels()
        return {"status": "success", "message": "All channels deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/content/generate")
async def generate_content(request: ContentGenerationRequest):
    """Generate content for specific audience and type"""
    try:
        from integrated_content_generator import ContentGenerator
        
        generator = ContentGenerator()
        content = generator.generate_content(
            audience_group=request.audience_group,
            content_type=request.content_type,
            custom_prompt=request.custom_prompt
        )
        
        # Create preview ID
        import uuid
        preview_id = str(uuid.uuid4())
        
        return {
            "status": "success",
            "content": content,
            "preview_id": preview_id,
            "audience_group": request.audience_group,
            "content_type": request.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/content/publish")
async def publish_generated_content(request: ContentGenerationRequest):
    """Generate and immediately publish content"""
    try:
        from integrated_content_generator import ContentGenerator
        
        generator = ContentGenerator()
        content = generator.generate_content(
            audience_group=request.audience_group,
            content_type=request.content_type,
            custom_prompt=request.custom_prompt
        )
        
        # Add to database
        post_id = db.add_post(
            content=content,
            channel_id=request.channel_id,
            scheduled_time=request.scheduled_time or datetime.now(),
            media_path=None,
            media_type=None
        )
        
        return {
            "status": "success",
            "post_id": post_id,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/content/audiences")
async def get_audience_groups():
    """Get available audience groups"""
    return {
        "audiences": [
            "Новички в дизайне",
            "Junior дизайнеры", 
            "Фрилансеры",
            "Разработчики"
        ]
    }

@app.get("/api/content/types")
async def get_content_types():
    """Get available content types"""
    return {
        "content_types": [
            "Проблема",
            "Решение",
            "Преимущества курса",
            "Кейс",
            "Совет",
            "Мотивация"
        ]
    }

@app.get("/api/content/analytics")
async def get_content_analytics():
    """Get content generation analytics"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Posts by audience (if we add audience tracking)
    cursor.execute("""
        SELECT COUNT(*) as total_posts,
               COUNT(CASE WHEN published = TRUE THEN 1 END) as published_posts,
               COUNT(CASE WHEN error_message IS NOT NULL THEN 1 END) as failed_posts
        FROM posts
    """)
    
    stats = cursor.fetchone()
    conn.close()
    
    return {
        "total_posts": stats[0],
        "published_posts": stats[1], 
        "failed_posts": stats[2],
        "success_rate": (stats[1]/stats[0]*100 if stats[0] > 0 else 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 