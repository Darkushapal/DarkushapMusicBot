from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag


active_throttling_chats = []


class throttling_antispam_middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        throttling_key = get_flag(data, "throttling_key")
        print(throttling_key, active_throttling_chats)
        if throttling_key is not None:
            if throttling_key == 'default':
                if event.chat.id in active_throttling_chats:
                    return
                else:
                    active_throttling_chats.append(event.chat.id)
            elif throttling_key == 'end':
                active_throttling_chats.remove(event.chat.id)
        print(throttling_key, active_throttling_chats)
        return await handler(event, data)
