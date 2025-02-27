import yt_dlp
import os
import re

from aiogram.types import FSInputFile


video_dir = 'for_files'


def downloader(url, info):
    video_title = info.get('title')
    video_duration = info.get('duration')
    
    video_file = f"{video_title}.mp3"
    video_file = re.sub(r'[\/:*?"<>|]', '_', video_file)
    video_path = os.path.join(video_dir, video_file)

    options = {
        'format': 'bestaudio/best' if video_duration <= 1000 else 'worstaudio/worst',
        'outtmpl': f'{video_path}',
        'noplaylist': True,
    }

    ydl = yt_dlp.YoutubeDL(options)
    ydl.download([url])

    final_audio = FSInputFile(video_path)

    return (final_audio,
            video_duration,
            video_title,
            video_path
            )


