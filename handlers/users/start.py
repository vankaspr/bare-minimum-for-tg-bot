"""
    Handler for command --> /start
    Handler for callback --> menu:home
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import menu_kb
from services import add_only_back_button
from settings.middlewares import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Main menu"""
    sms = "Всем велком -_-"
    logger.info("Выкатываем главное меню.")
    await message.answer(sms, reply_markup=menu_kb(message.from_user.id))


@router.callback_query(F.data == "menu:home")
async def cmd_back_to_home(
        call: CallbackQuery):
    """Return to main menu"""
    await call.answer()
    logger.info("Вернулись в главное меню.")
    await call.message.edit_text(
        "Вы вернулись в главное меню 🤸🏻",
        reply_markup=menu_kb(call.from_user.id)
    )

@router.message(F.text.lower() == "/help")
async def get_help(message: Message):
    """Help cmd"""
    logger.info("Выкатываем список команд")
    sms = (
        f"Возможности и опции бота:\n\n"
        f"Команда <b>/support</b> пригодится если вы столкнулись "
        f"с какой-то проблемой при взаимодействии с ботом.\n\n"
        f"Команда <b>...</b>"
    )
    await message.answer(
        sms,
        reply_markup=add_only_back_button(),
        parse_mode="HTML"
    )
    #TODO: оформить обработчик html