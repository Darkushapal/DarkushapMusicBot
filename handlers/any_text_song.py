import yt_dlp
import os

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.downloader import downloader
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from keyboards.simple_row_keyboard import make_row_keyboard

router = Router()

ydl_opts = {
    "extract_flat": True,
}


class FindSong(StatesGroup):
    choosing_song_name = State()


class UsingBot(StatesGroup):
    getting_info = State()


@router.message(StateFilter(None), F.text, flags={'long_operation': 'upload_video_note'})
async def url_msg(message: Message, state: FSMContext):
    await state.set_state(UsingBot.getting_info)
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    search_name = f"ytsearch5:{message.text}"
    info = ydl.extract_info(search_name, download=False)['entries'][0:5]

    search_results = ''
    counter = 0
    for i in info:
        counter += 1
        search_results = f'{search_results}{i.get("title")}\n'

    await message.answer(
        text=f'Выберите нужное название:\n{search_results}',
        reply_markup=make_row_keyboard(i.get("title") for i in info),
        )
    await state.set_state(FindSong.choosing_song_name)
    await state.update_data(info=info)


@router.message(
    FindSong.choosing_song_name
)
async def song_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    info = user_data["info"]
    info_titles = list((i.get("title") for i in info))

    if message.text not in info_titles:
        await message.answer(
            text="Выберите нужное название на клавиатуре"
        )
        return

    sent_message = await message.answer(
        text=f"Вы выбрали {message.text.lower()}. \n"
             f"Скачиваю :]",
        reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(UsingBot.getting_info)

    index_of_song = info_titles.index(message.text)
    info = info[index_of_song]
    url = info.get('url')

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
