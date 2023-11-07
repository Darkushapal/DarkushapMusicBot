import yt_dlp
import os
import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile

video_dir = 'for_files'


def downloader(message: Message, url, info):
    ydl = yt_dlp.YoutubeDL()

    video_title = info.get('title')
    video_duration = info.get('duration')
    video_file = f"{video_title}.mp3"
    video_file = re.sub(r'[\/:*?"<>|]', '_', video_file)
    video_path = os.path.join(video_dir, video_file)
    options = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': f'{video_path}',
            'noplaylist': True,
        }
    ydl = yt_dlp.YoutubeDL(options)
    ydl.download([url])

    final_audio = FSInputFile(video_path)

    return (final_audio,
            video_duration,
            video_title,
            )

    if os.path.exists(video_path):
        os.remove(video_path)

