from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.services import add_back_to_home_button


def support_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Есть ещё проблемы?", callback_data="menu:support"
                )
            ],
        ]
    )
    return add_back_to_home_button(menu)
