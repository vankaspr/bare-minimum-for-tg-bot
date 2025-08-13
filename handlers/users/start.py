from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import menu_kb
from settings.middlewares import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Main menu"""
    sms = "hihi"
    logger.info("Выкатываем главное меню.")
    await message.answer(sms, reply_markup=menu_kb(message.from_user.id))

@router.callback_query(F.data == "home")
async def cmd_back_to_home(call: CallbackQuery):
    """Return to main menu"""
    await call.answer()
    logger.info("Вернулись в главное меню.")
    await call.message.edit_text(
        "Вы вернулись в главное меню 🤸🏻",
        reply_markup=menu_kb(call.from_user.id)
    )