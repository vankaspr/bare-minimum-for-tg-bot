from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.crud import get_user_by_id, get_user_by_username
from services.add_back_button import add_only_back_button
from settings.middlewares import logger


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


@auxiliary_router.message(UserSearch.waiting_for_id)
async def process_user_id(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    try:
        user_id = int(message.text.strip())
        user = await get_user_by_id(session, user_id)

        if not user:
            await message.answer(
                "❌ Пользователь не найден",
                reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:found_user")
            )
            logger.debug("Пользователь не найден")
            return

        await message.answer(
            f"👤 Найден пользователь:\n\n"
            f"ID: {user.id}\n"
            f"Username: @{user.username}\n"
            f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
            # reply_markup= клавиатура с действиями для пользователя (забанить написать и тд)
        )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ ID должен быть числом. Попробуйте еще раз:",
            reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:found_user")
        )

@auxiliary_router.message(UserSearch.waiting_for_query)
async def process_username(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    username = message.text.strip().lstrip("@")

    if not username:
        await message.answer(
            "❌ Username не может быть пустым. Попробуйте еще раз:",
            reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:found_user")
        )
        return

    user = await get_user_by_username(session, username)

    if not user:
        await message.answer(
            "❌ Пользователь не найден",
            reply_markup=add_only_back_button(text="← Назад", callback_data="admin:found_user")
        )
        logger.debug("Пользователь не найден")
        return

    await message.answer(
        f"👤 Найден пользователь:\n\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
    )

    await state.clear()
