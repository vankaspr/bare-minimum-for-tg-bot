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

def users_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Найти гада", callback_data=f"admin:user_profile"),
                InlineKeyboardButton(text="📊 Статистика", callback_data=f"admin:warn_user")
            ],
            [
                InlineKeyboardButton(text="⚠️ Активные баны", callback_data=f"admin:timeout"),
                InlineKeyboardButton(text="🚫 Забанить", callback_data=f"admin:user_stats")
            ]
        ]
    )

    return add_back_to_home_button(menu)