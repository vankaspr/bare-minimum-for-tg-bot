from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters import IsAdmin
from keyboards import admin_kb
from settings.middlewares import logger


admin_router = Router()

@admin_router.callback_query(F.data == "admin:admin")
async def admin(callback: CallbackQuery):
    """Get admin keyboards"""
    if not IsAdmin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return
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
    if not IsAdmin(message.from_user.id):
        await message.answer("Доступ запрещен", show_alert=True)
        return
    await message.answer(
        "Админ-панель...\n"
        "В разработке...⛏️",
        reply_markup=admin_kb()
    )
