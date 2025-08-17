"""
    Handler for command --> /start
    Handler for callback --> menu:home
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import get_or_create_user
from filters.ban_check import BannedUserFilter
from keyboards import menu_kb
from services import add_only_back_button
from settings.middlewares import logger


router = Router()
router.message.filter(BannedUserFilter())
router.callback_query.filter(BannedUserFilter())

@router.message(CommandStart())
async def cmd_start(
        message: Message,
        session: AsyncSession
):
    """Main menu"""
    user = await get_or_create_user(session, message.from_user)
    sms = "Всем велком -_-"
    logger.debug(f"Привет, {user.username or user.id}! Ты добавлен в базу данных.")
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