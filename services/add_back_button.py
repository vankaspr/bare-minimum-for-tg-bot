from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_back_to_home_button(
        keyboard: InlineKeyboardMarkup,
        text: str = "← Назад в меню",
        callback_data: str = "menu:home"
) -> InlineKeyboardMarkup:
    """ADD button back to home/main menu"""
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
    )
    return keyboard
