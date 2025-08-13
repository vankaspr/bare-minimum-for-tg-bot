from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import add_back_to_home_button


def admin_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin:stats")],
            [InlineKeyboardButton(text="🔨 Пользователи", callback_data="admin:users")],
            [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin:broadcast")],
            [InlineKeyboardButton(text="🚨 Логи ошибок", callback_data="admin:error_logs")],
            [InlineKeyboardButton(text="💰 Платежи", callback_data="admin:payments")],
        ]
    )

    return add_back_to_home_button(menu)