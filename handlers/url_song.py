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
    ydl = yt_dlp.YoutubeDL()
    url = message.text
    info = ydl.extract_info(url, download=False)

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
        title=title
    )

    await sent_message.delete()

    if os.path.exists(video_path):
        os.remove(video_path)

    await state.clear()
