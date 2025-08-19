from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import admin
from src.core.middlewares import logger
from src.core.filters import AdminFilter

admin_filter = AdminFilter(admin_ids=[admin])


def menu_kb(user_id) -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ТехПод ⚙️", callback_data="menu:support")],
        ]
    )

    if admin_filter.check_user_id(user_id):
        logger.info(f"Батя в здании, допаем красную кнопку.")
        menu.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🎀 Админ-панель 🎀", callback_data="admin:admin"
                )
            ]
        )

    return menu
