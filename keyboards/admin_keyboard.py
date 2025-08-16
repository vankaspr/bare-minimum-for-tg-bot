from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services import add_back_to_home_button, add_back_to_admin_button


def admin_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
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
                InlineKeyboardButton(text="🔍 Найти гада", callback_data="admin:found_user"),
            ],
            [
                InlineKeyboardButton(text="⚠️ Активные баны", callback_data="admin:active_ban"),
            ]
        ]
    )

    return add_back_to_admin_button(menu)

def search_user_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="По ID", callback_data="admin:search_by_id")],
            [InlineKeyboardButton(text="По Username", callback_data="admin:search_by_username")]
        ]
    )

    return add_back_to_admin_button(menu)

def users_actions_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Забанить", callback_data="admin:user_ban")],
            [InlineKeyboardButton(text="Разбанить", callback_data="admin:user_unban")],
            [InlineKeyboardButton(text="Написать", callback_data="admin:user_mes")],
        ]
    )

    return add_back_to_admin_button(menu)

def confirm_kb():
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="admin:confirm_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="admin:confirm_no"),
            ]
        ]
    )
    return add_back_to_admin_button(menu)