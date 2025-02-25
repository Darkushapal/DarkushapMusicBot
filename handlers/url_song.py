import yt_dlp
import os

from aiogram import Router, F
from aiogram.types import Message
from handlers.downloader import downloader
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


class UsingBot(StatesGroup):
    getting_info = State()


@router.message(StateFilter(None), F.entities[0].type == 'url', flags={'long_operation': 'upload_video_note'})
async def url_msg(message: Message, state: FSMContext):
    await state.set_state(UsingBot.getting_info)
    url = message.text

    # Check if the URL is a YouTube link
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.answer("Эй, я же попросил ссылку на ютуб (ノಠ益ಠ)ノ")
        await state.clear()
        return

    ydl = yt_dlp.YoutubeDL()
    info = ydl.extract_info(url, download=False)

    # Fetch the author of the song
    author = info.get("uploader", "Unknown Artist")  # Default to "Unknown Artist" if not found

    if info.get("duration") > 4000:
        await message.answer("Ваше видео слишком долгое, пожалуйста, пожалейте бота :[")
        await state.clear()
        return
    sent_message = await message.answer("Скачиваю :]")

    # call downloader and take info of video
    audio, duration, title, video_path = downloader(
        url=url,
        info=info
    )

    await message.answer_audio(
        audio=audio,
        duration=duration,
        title=title,
        performer=author  # Include the author in the audio message
    )

    await sent_message.delete()

    if os.path.exists(video_path):
        os.remove(video_path)

    await state.clear()
