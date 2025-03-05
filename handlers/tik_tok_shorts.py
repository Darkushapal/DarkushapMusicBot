import re
import os
import yt_dlp

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

# Directory for storing videos temporarily
video_dir = 'for_files'
os.makedirs(video_dir, exist_ok=True)

# Regex patterns for TikTok and YouTube Shorts URLs
TIKTOK_PATTERN = r'https?://(?:www\.)?(?:tiktok\.com|vm\.tiktok\.com)/(?:@[\w.]+/video/|t/|v/|embed/|video/|)(\d+)'
YOUTUBE_SHORTS_PATTERN = r'https?://(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)'


class VideoDownload(StatesGroup):
    downloading = State()


@router.message(
    StateFilter(None), 
    F.text.regexp(TIKTOK_PATTERN) | F.text.regexp(YOUTUBE_SHORTS_PATTERN),
    flags={'long_operation': 'upload_video'}
)
async def handle_video_links(message: Message, state: FSMContext):
    """Handler for TikTok and YouTube Shorts links"""
    await state.set_state(VideoDownload.downloading)
    url = message.text
    
    # Configure yt-dlp with cookies for YouTube
    ydl_opts = {
        'cookiefile': 'www.youtube.com_coockies.txt' if 'youtube.com' in url else None
    }
    
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    try:
        # Extract video information
        info = ydl.extract_info(url, download=False)
        
        # Check video duration
        if info.get("duration", 0) > 4000:
            await message.answer("Видео слишком длинное, пожалуйста, пожалейте бота :[")
            await state.clear()
            return
        
        sent_message = await message.answer("Скачиваю видео :]")
        
        # Determine video type for better user feedback
        video_type = "YouTube Shorts" if "youtube.com/shorts" in url else "TikTok"
        
        # Download the video
        from handlers.downloader import downloader
        video_file, duration, title, video_path = downloader(
            url=url,
            info=info
        )
        
        # Get the author/uploader
        author = info.get("uploader", "Unknown")
        
        # Send the video to the user
        await message.answer_video(
            video=video_file,
            duration=duration,
            caption=f"{title}\nАвтор: {author}"
        )
        
        await sent_message.delete()
        
        # Clean up the file
        if os.path.exists(video_path):
            os.remove(video_path)
            
    except Exception as e:
        await message.answer(f"Ошибка при скачивании видео: {str(e)}")
    
    finally:
        await state.clear() 