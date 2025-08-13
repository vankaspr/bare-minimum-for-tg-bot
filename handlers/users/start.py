from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import menu_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    sms = "hihi"
    await message.answer(sms, reply_markup=menu_kb(message.from_user.id))