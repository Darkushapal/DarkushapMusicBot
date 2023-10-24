import yt_dlp
import os
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

router = Router()

video_dir = 'for_files'

options = {
    'format': 'ba',
    'outtmpl': f'{video_dir}/%(title)s.mp3',
    'playlist_items': "0:1"
}


@router.message(F.text, flags={"long_operation": "upload_video_note"})
async def downloader(message: Message):
    url = message.text
    tiny_url = url.split('&')

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    if len(tiny_url) > 1:
        video_title = info['entries'][0]['title']
    else:
        video_title = info.get('title')

    video_file = f'{video_title}.mp3'
    video_path = f'{video_dir}\{video_file}'

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)

    audio_final = FSInputFile(video_path)

    await message.reply_audio(audio_final)

    os.remove(video_path)
