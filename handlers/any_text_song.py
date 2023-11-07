import yt_dlp

from aiogram import Router, F
from aiogram.types import Message
from handlers.downloader import downloader
from aiogram.methods.send_audio import SendAudio

router = Router()

ydl_opts = {
    "extract_flat": True,
}


@router.message(F.text, flags={'throttling_key': 'default'})
async def url_msg(message: Message):
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    url = f"ytsearch5:{message.text}"
    info = ydl.extract_info(url, download=False)['entries'][0:5]
    info.get('title')

    downloaded_info = downloader(
        message,
        url=url,
        info=info
    )
    await bot.SendAudio
