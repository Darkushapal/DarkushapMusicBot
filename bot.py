import asyncio
from aiogram import Bot, Dispatcher
import logging
from config import config
from handlers import start, url_song, any_text_song
from middlewares.long_operation_middleware import ChatActionMiddleware
from middlewares.throttling_middleware import throttling_antispam_middleware

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(start.router, url_song.router, any_text_song.router)
    dp.message.middleware(ChatActionMiddleware())
    #dp.message.middleware(throttling_antispam_middleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
