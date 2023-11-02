import yt_dlp

from aiogram import Router, F
from aiogram.types import Message
from handlers.downloader import downloader


router = Router()


@router.message(F.text)
async def url_msg(message: Message):
    ydl = yt_dlp.YoutubeDL()
    url = f"ytsearch1:{message.text}"
    info = ydl.extract_info(url, download=False)['entries'][0]

    await downloader(
        message,
        url=url,
        info=info
        )
