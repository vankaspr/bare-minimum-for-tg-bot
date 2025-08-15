from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from services.add_back_button import add_only_back_button

auxiliary_router = Router()


class UserSearch(StatesGroup):
    waiting_for_query = State()
    waiting_for_id = State()


@auxiliary_router.callback_query(F.data == "admin:search_by_id")
async def request_user_by_id(
        callback: CallbackQuery,
        state: FSMContext
):
    """Found user by ID"""
    await callback.answer()
    await callback.message.answer(
        "Введите ID пользователя:",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )
    await state.set_state(UserSearch.waiting_for_id)


@auxiliary_router.callback_query(F.data == "admin:search_by_username")
async def request_user_by_username(
        callback: CallbackQuery,
        state: FSMContext
):
    """Found user by username"""
    await callback.answer()
    await callback.message.answer(
        "Введите username (без @):",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )
    await state.set_state(UserSearch.waiting_for_query)