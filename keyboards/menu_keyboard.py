from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from filters import IsAdmin
from services import add_back_to_home_button
from settings.middlewares import logger


def menu_kb(user_id) -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='ТехПод ⚙️',callback_data="menu:support")],
        ]
    )

    if IsAdmin(user_id):
        logger.info(f"Батя в здании, допаем красную кнопку.")
        menu.inline_keyboard.append(
            [InlineKeyboardButton(text='🎀 Админ-панель 🎀',callback_data='admin:admin')]
        )

    return menu


def support_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Есть ещё проблемы?", callback_data="menu:support")],
        ]
    )
    return add_back_to_home_button(menu)