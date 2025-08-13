from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from settings.middlewares import logger


def menu_kb(user_id) -> InlineKeyboardMarkup:
    from filters import IsAdmin
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
