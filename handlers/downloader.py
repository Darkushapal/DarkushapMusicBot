import yt_dlp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


router = Router()

url = "https://www.youtube.com/watch?v=RYCR55P99yg"

options = {'format': "ba"}


@router.callback_query(F.data, flags={"long_operation": "upload_video_note"})
async def downloader(message: Message, callback: CallbackQuery):
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)
