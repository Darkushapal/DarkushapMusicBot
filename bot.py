import asyncio
from aiogram import Bot, Dispatcher
import logging
from config import config
from handlers import questions, diff_types, group_games, forwarded_from_channel, downloader
from middlewares.long_operation_middleware import ChatActionMiddleware

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(questions.router, diff_types.router, group_games.router, forwarded_from_channel.router, downloader.router)
    dp.message.middleware(ChatActionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
