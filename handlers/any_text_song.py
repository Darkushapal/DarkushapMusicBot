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

    search_results = ''
    counter = 0
    for i in info:
        counter += 1
        search_results = f'{search_results}{counter}) {i.get("title")}\n'

    await message.answer(
        text=f'Выберите нужное название:\n{search_results}'
        )


    # give a state, waiting for a response

    # make a keyboard
"""
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
"""