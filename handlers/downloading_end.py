from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message



@flags.throttling_key('end')
async def cmd_end(message: Message):
    await message.answer(
        text="Можете скачать ещё песен!",
        )