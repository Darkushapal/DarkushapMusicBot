from aiogram import Router, F
from aiogram.types import Message, Chat
import time

router = Router()


@router.message(F.forward_from_chat[F.type == "channel"].as_("channel"), flags={"long_operation": "upload_video_note"})
async def forwarded_from_channel(message: Message, channel: Chat):
    await message.answer(f"This channel's ID is {channel.id}")