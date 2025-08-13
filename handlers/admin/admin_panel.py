"""
    Handler for command --> /admin
    Handler for callback --> admin:admin
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.is_admin import IsAdmin
from keyboards import admin_kb
from settings.middlewares import logger
from config import admin

admin_router = Router()
admin_router.callback_query.filter(IsAdmin(admin))


@admin_router.callback_query(F.data == "admin:admin")
async def admin(callback: CallbackQuery):
    """Get admin keyboards"""
    await callback.answer()
    logger.info("Получении админ-панели с колбэка")
    await callback.message.answer(
        "Админ-панель...\n"
        "В разработке...⛏️",
        reply_markup=admin_kb()
    )


@admin_router.message(F.text == "/admin")
async def admin_panel(message: Message):
    logger.info("Получении админ-панели с команды")

    await message.answer(
        "Админ-панель...\n"
        "В разработке...⛏️",
        reply_markup=admin_kb()
    )


@admin_router.callback_query(F.data == "admin:stats")
async def get_admin_stats(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получении статистики с колбэка")
    await callback.message.answer(
        "Здесь будет лежать статистика",
    )

@admin_router.callback_query(F.data == "admin:users")
async def get_admin_users(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получении раздела о пользователях с колбэка")
    await callback.message.answer(
        "Здесь будет лежать ещё одна клавиатура"
        "Где будет всё про пользователей",
    )

@admin_router.callback_query(F.data == "admin:broadcast")
async def get_admin_broadcast(callback: CallbackQuery):

    await callback.answer()
    logger.info("Создать рассылку с колбэка")
    await callback.message.answer(
        "Здесь будет лежать приблуда для создания рассылок",
    )

@admin_router.callback_query(F.data == "admin:error_logs")
async def get_admin_logs(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получение последних логов с колбэка")
    await callback.message.answer(
        "Здесь будет лежать какое-то количество логов, "
        "которые всегда можно будет посмотреть",
    )


@admin_router.callback_query(F.data == "admin:payments")
async def get_admin_payments(callback: CallbackQuery):

    await callback.answer()
    logger.info("Получении информации о платежах с колбэка")
    await callback.message.answer(
        "Здесь будет лежать инфа о платежах"
        "На случай если я включу платежи",
    )
