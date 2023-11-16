from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="Используйте ссылку или напишите название нужной вам песни и исполнителя",
        )
