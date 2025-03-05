import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import config
from handlers import start, url_song, any_text_song, tik_tok_shorts
from middlewares.long_operation_middleware import ChatActionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, url_song.router, any_text_song.router, tik_tok_shorts.router)
    dp.message.middleware(ChatActionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
