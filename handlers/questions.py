from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.for_questions import get_yes_no_kb

import time

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="Вы довольны своей работой?",
        reply_markup=get_yes_no_kb()
    )


@router.message(F.text.lower() == "да")
async def questions_answer_yes(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "нет", flags={"long_operation": "upload_video_note"})
async def question_answer_no(message: Message):
    await message.answer(
        "УВЫ. ГОРНИЛО",
        reply_markup=ReplyKeyboardRemove()
    )
