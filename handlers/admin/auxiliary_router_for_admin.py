from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
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


@auxiliary_router.message(UserSearch.waiting_for_id)
async def process_user_id(
        message: Message,
        state: FSMContext
):
    try:
        user_id = int(message.text)
        # Здесь должен быть поиск пользователя в БД
        #
        user = {"id": user_id, "username": "test_user"} # Заглушка

        await message.answer(
            f"👤 Найден пользователь:\n\n"
            f"ID: {user['id']}\n"
            f"Username: @{user['username']}",
            # reply_markup= клавиатура с действиями для пользователя (забанить написать и тд)
        )

        await state.clear()

    except ValueError:
        await message.answer("❌ ID должен быть числом. Попробуйте еще раз:",
                             reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:found_user"))

@auxiliary_router.message(UserSearch.waiting_for_query)
async def process_username(
        message: Message,
        state: FSMContext
):
    username = message.text.strip()
    if not username:
        await message.answer(
            "❌ Username не может быть пустым. Попробуйте еще раз:",
            reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:found_user")
        )
        return

    # Здесь должен быть поиск пользователя в БД
    #
    user = {"id": 123456, "username": "test_user"}  # Заглушка

    await message.answer(
        f"👤 Найден пользователь:\n\n"
        f"ID: {user['id']}\n"
        f"Username: @{user['username']}",
    )

    await state.clear()
