import yt_dlp

from aiogram import Router, F
from aiogram.types import Message
from handlers.downloader import downloader


router = Router()


@router.message(F.entities[0].type == 'url')
async def url_msg(message: Message):
    ydl = yt_dlp.YoutubeDL()
    url = message.text
    info = ydl.extract_info(url, download=False)

    await downloader(
        message,
        url=url,
        info=info
        )


