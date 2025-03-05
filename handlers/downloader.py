import yt_dlp
import os
import re

from aiogram.types import FSInputFile


video_dir = 'for_files'
os.makedirs(video_dir, exist_ok=True)


def downloader(url, info):
    video_title = info.get('title')
    video_duration = info.get('duration')
    
    # Determine if it's a TikTok or YouTube Shorts video
    is_video = "tiktok.com" in url or "vm.tiktok.com" in url or "youtube.com/shorts" in url
    
    # Set file extension based on content type
    file_extension = ".mp4" if is_video else ".mp3"
    
    # Clean the filename
    video_file = f"{video_title}{file_extension}"
    video_file = re.sub(r'[\/:*?"<>|]', '_', video_file)
    video_path = os.path.join(video_dir, video_file)

    # Set different options based on content type
    if is_video:
        options = {
            'format': 'best[ext=mp4]/best' if video_duration <= 1000 else 'worst[ext=mp4]/worst',
            'outtmpl': f'{video_path}',
            'noplaylist': True,
        }
    else:
        options = {
            'format': 'bestaudio/best' if video_duration <= 1000 else 'worstaudio/worst',
            'outtmpl': f'{video_path}',
            'noplaylist': True,
        }

    ydl = yt_dlp.YoutubeDL(options)
    ydl.download([url])

    final_file = FSInputFile(video_path)

    return (final_file,
            video_duration,
            video_title,
            video_path
            )


