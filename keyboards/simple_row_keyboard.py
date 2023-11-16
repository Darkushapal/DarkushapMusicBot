from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:

    row = [KeyboardButton(text=str(item)) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

# несколько уровней