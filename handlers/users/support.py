"""
    Handler for command --> /support
"""
from datetime import datetime
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import support_group_id

from settings import bot
from settings.middlewares import logger

support_router = Router()


class SupportForm(StatesGroup):
    waiting_for_issue = State()


@support_router.message(F.text.lower() == "/support")
async def cmd_process_support_request(
        message: Message,
        state: FSMContext
):
    await state.set_state(SupportForm.waiting_for_issue)
    await message.answer("Опишите вашу проблему в одном сообщении.")


@support_router.message(F.text, SupportForm.waiting_for_issue)
async def process_support(
        message: Message,
        state: FSMContext
):
    user_issue = message.text
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    logger.info("Штопаем саппорт-клаву, получаем сообщение в саппорт-канал")
    await message.answer(
        "Перенаправили ваш запрос в тех.поддержку!\n"
        "Решим проблему как только, так сразу 😇",
    )


    await bot.send_message(
        support_group_id,
        f"⚠️ <b>Support</b> | New request\n\n"
        f"👤 From: @{message.from_user.username}\n\n"
        f"🆔 : <code>{message.from_user.id}</code>\n\n"
        f"📅 Date: {current_time}\n\n"
        f"<b>📩 Issue:</b>\n\n"
        f"<blockquote>{user_issue}</blockquote>",
        parse_mode="HTML"
    )

    await state.clear()