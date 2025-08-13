from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from filters import IsAdmin
from keyboards import menu_kb
from settings.middlewares import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Main menu"""
    sms = "hihi"
    logger.info("Выкатываем главное меню.")
    await message.answer(sms, reply_markup=menu_kb(message.from_user.id))

@router.callback_query(F.data == "menu:home")
async def cmd_back_to_home(call: CallbackQuery):
    """Return to main menu"""
    await call.answer()
    logger.info("Вернулись в главное меню.")
    await call.message.edit_text(
        "Вы вернулись в главное меню 🤸🏻",
        reply_markup=menu_kb(call.from_user.id)
    )

@router.callback_query(F.data == "menu:admin")
async def admin(callback: CallbackQuery):
    """Get admin keyboards"""
    if not IsAdmin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(
        "Админ-панель...\n"
        "В разработке...⛏️"
    )