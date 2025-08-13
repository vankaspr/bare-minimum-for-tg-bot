from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters import IsAdmin
from settings.middlewares import logger


def menu_kb(user_id) -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='ТехПод ⚙️',
                    callback_data="support_request"
                )
            ]
        ]
    )

    if IsAdmin(user_id):
        logger.info(f"Батя в здании, допаем красную кнопку.")
        menu.inline_keyboard.append(
            [InlineKeyboardButton(
                text='🎀 Админ-панель 🎀',
                callback_data='admin'
            )]
        )

    return menu

