import yt_dlp
import os

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

router = Router()

video_dir = 'for_files'

options = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': f'{video_dir}/%(title)s.mp3',
    'noplaylist': True,
}


@router.message(F.text, flags={"long_operation": "upload_video_note"})
async def downloader(message: Message):
    ydl = yt_dlp.YoutubeDL(options)
    if message.entities is not None:
        url = message.text
        info = ydl.extract_info(url, download=False)

    else:
        info = ydl.extract_info(f"ytsearch1:{message.text}", download=False)['entries'][0]
        url = info.get('url')
        ydl.download(f"ytsearch1:{message.text}")

    video_title = info.get('title')
    video_duration = info.get('duration')
    video_file = f"{video_title}.mp3"
    video_path = f"{video_dir}\\{video_file}"

    if video_duration > 1200:
        await message.answer(
            text="Слишком долгое видео, пожалейте бота :["
        )

    else:
        ydl.download(url)

        final_audio = FSInputFile(video_path)

        await message.answer_audio(
                audio=final_audio,
                duration=video_duration,
                title=video_title,
        )

        os.remove(video_path)
