import asyncio
from aiogram import Bot, Dispatcher
import logging
from config import config
from handlers import start, url_song, any_text_song, downloader
from middlewares.long_operation_middleware import ChatActionMiddleware

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(start.router, url_song.router, any_text_song.router, downloader.router)
    dp.message.middleware(ChatActionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
