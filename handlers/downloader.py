import yt_dlp
import os
import re

from aiogram import Router
from aiogram.types import Message
from aiogram.types import FSInputFile

router = Router()

video_dir = 'for_files'


@router.message(flags={"long_operation": "upload_video_note"})
async def downloader(message: Message, url, info):
    ydl = yt_dlp.YoutubeDL()

    video_title = info.get('title')
    video_duration = info.get('duration')
    video_file = f"{video_title}.mp3"
    video_file = re.sub(r'[\/:*?"<>|]', '_', video_file)
    video_path = os.path.join(video_dir, video_file)

    if video_duration > 1200:
        await message.answer(
            text="Слишком долгое видео, пожалейте бота :["
        )

    else:
        options = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': f'{video_path}',
            'noplaylist': True,
        }
        ydl = yt_dlp.YoutubeDL(options)
        ydl.download([url])

        final_audio = FSInputFile(video_path)

        await message.bot.send_audio(
            chat_id=message.chat.id,
            audio=final_audio,
            duration=video_duration,
            title=video_title,
        )

        if os.path.exists(video_path):
            os.remove(video_path)
