"""
    Handler for command --> /admin
    Handler for callback --> admin:admin
    Handler for callback --> admin:users
                                --> admin:found_user
                                --> admin:user_stats
                                --> admin:active_ban
                                --> admin:user_ban
    Handler for callback --> admin:error_logs
    Handler for callback --> admin:payments
    Handler for callback --> admin:broadcast
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from filters.is_admin import IsAdmin
from keyboards import admin_kb, users_kb
from keyboards.admin_keyboard import search_user_kb
from services import add_back_to_home_button, add_only_back_button
from settings.middlewares import logger
from config import admin
from utilities.error_logs import get_error_logs


admin_router = Router()
admin_router.callback_query.filter(IsAdmin(admin))


# --- Главное меню ---
@admin_router.callback_query(F.data == "admin:admin")
@admin_router.message(F.text == "/admin")
async def admin(update: Message | CallbackQuery):
    """Get admin keyboards"""
    if isinstance(update, CallbackQuery):
        logger.info("Получении админ-панели с колбэка")
        await update.answer()
        message = update.message
    else:
        logger.info("Получении админ-панели с команды")
        message = update

    await message.answer("Админ-панель ⛏️",reply_markup=admin_kb())


# --- Раздел пользователей ---
@admin_router.callback_query(F.data == "admin:users")
async def get_admin_users(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получении раздела о пользователях с колбэка")
    await callback.message.answer(
        "🛠 Управление пользователями",
        reply_markup=users_kb()
    )

@admin_router.callback_query(F.data == "admin:found_user")
async def found_user(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🔍 Выберите способ поиска:",
        reply_markup=search_user_kb()
    )


@admin_router.callback_query(F.data == "admin:user_stats")
async def get_stats(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Тут лежит статистика активности пользователей")


@admin_router.callback_query(F.data == "admin:active_ban")
async def get_active_ban(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Тут мы смотрим кого забанили")


@admin_router.callback_query(F.data == "admin:user_ban")
async def ban_user(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Тут мы баним блядей")


# --- Системные функции ---
@admin_router.callback_query(F.data == "admin:error_logs")
async def get_admin_logs(callback: CallbackQuery):
    await callback.answer("⏳ Загружаю логи...")

    logs = await get_error_logs()

    if not logs:
        await callback.message.answer(
            "📭 Нет свежих ошибок ERROR/WARNING/DEBUG",
        )

    await callback.message.answer(
        f"<b>Последние ошибки:</b>\n"
        f"<pre>{logs}</pre>",
        parse_mode="HTML",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )
# --- Дополнительные разделы ---
@admin_router.callback_query(F.data == "admin:payments")
async def get_admin_payments(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получении информации о платежах с колбэка")
    await callback.message.answer(
        "Здесь будет лежать инфа о платежах"
        "На случай если я включу платежи",
    )

@admin_router.callback_query(F.data == "admin:broadcast")
async def get_admin_broadcast(callback: CallbackQuery):

    await callback.answer()
    logger.info("Создать рассылку с колбэка")
    await callback.message.answer(
        "Здесь будет лежать приблуда для создания рассылок",
    )
