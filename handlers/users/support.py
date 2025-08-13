"""
    Handler for command --> /support
    Handler for callback --> menu:support
"""

from typing import Union
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from services import process_support_message

support_router = Router()


class SupportForm(StatesGroup):
    waiting_for_issue = State()


@support_router.message(F.text.lower() == "/support")
@support_router.callback_query(F.data == "menu:support")
async def cmd_process_support_request(
        event: Union[Message, CallbackQuery],
        state: FSMContext
):
    """Handle /support command"""
    if isinstance(event, CallbackQuery):
        await event.answer()
        message = event.message
    else:
        message = event

    await state.set_state(SupportForm.waiting_for_issue)
    await message.answer(
        "Опишите вашу проблему в одном сообщении."
    )


@support_router.message(F.text, SupportForm.waiting_for_issue)
async def process_support(
        message: Message,
        state: FSMContext,
):
    await process_support_message(message)
    await state.clear()
