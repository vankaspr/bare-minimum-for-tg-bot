from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_back_to_home_button(
    keyboard: InlineKeyboardMarkup,
    text: str = "← Назад в меню",
    callback_data: str = "menu:home",
) -> InlineKeyboardMarkup:
    """ADD button back to home/main menu"""
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
    )
    return keyboard


def add_back_to_admin_button(
    keyboard: InlineKeyboardMarkup,
    text: str = "← Отмена",
    callback_data: str = "admin:admin",
) -> InlineKeyboardMarkup:
    """ADD button back to admin menu"""
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=text, callback_data=callback_data)]
    )
    return keyboard


def add_only_back_button(
    text: str = "← Назад в меню", callback_data: str = "menu:home"
):
    """Create one button to back to home or admin or whatever"""
    back = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=callback_data)]]
    )
    return back
