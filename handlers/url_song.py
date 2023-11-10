import yt_dlp

from aiogram import Router, F
from aiogram.types import Message
from handlers.downloader import downloader
from aiogram.methods.send_audio import SendAudio

router = Router()


@router.message(F.entities[0].type == 'url', flags={'throttling_key': 'default'})
async def url_msg(message: Message):
    ydl = yt_dlp.YoutubeDL()
    url = message.text
    info = ydl.extract_info(url, download=False)
    await message.answer("Скачиваю")

    # call downloader and take info of video
    audio, duration, title = downloader(
        message=message,
        url=url,
        info=info
    )

    await message.answer_audio(
        audio=audio,
        duration=duration,
        title=title
    )
