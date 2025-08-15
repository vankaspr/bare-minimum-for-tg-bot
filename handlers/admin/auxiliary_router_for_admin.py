from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import admin
from database.crud import get_user_by_id, get_user_by_username
from filters import AdminFilter
from keyboards.admin_keyboard import users_actions_kb
from services.add_back_button import add_only_back_button
from settings.middlewares import logger

auxiliary_router = Router()
auxiliary_router.callback_query.filter(AdminFilter(admin))
auxiliary_router.message.filter(AdminFilter(admin))


class UserSearch(StatesGroup):
    waiting_for_query = State()
    waiting_for_id = State()
    waiting_for_ban_confirmation = State()
    waiting_for_unban_confirmation = State()
    waiting_for_message = State()


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

        await state.update_data(user_id=user.id, username=user.username)

        await message.answer(
            f"👤 Найден пользователь:\n\n"
            f"ID: {user.id}\n"
            f"Username: @{user.username}\n"
            f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
            reply_markup=users_actions_kb()
        )


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

    await state.update_data(user_id=user.id, username=user.username)

    await message.answer(
        f"👤 Найден пользователь:\n\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
        reply_markup=users_actions_kb()
    )


# -------------------BAN AND UNBAN USER------------------------------------
@auxiliary_router.callback_query(F.data == "admin:user_ban")
async def request_to_ban_user(
        callback: CallbackQuery,
        state: FSMContext
):
    """Ban user by ID or Username"""
    await callback.answer()
    await callback.message.answer(
        "Забанить этого пользователя?",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )

    await state.set_state(UserSearch.waiting_for_ban_confirmation)


@auxiliary_router.callback_query(F.data == "admin:user_unban")
async def request_to_unban_user(
        callback: CallbackQuery,
        state: FSMContext
):
    """Unban user by ID or Username"""
    await callback.answer()
    await callback.message.answer(
        "Разбанить этого урода? Да или Нет?",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )
    await state.set_state(UserSearch.waiting_for_unban_confirmation)


@auxiliary_router.callback_query(F.data.startswith("admin:confirm_"), UserSearch.waiting_for_ban_confirmation)
async def confirm_ban_user(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    action = callback.data.split("_")[1]
    user_data = await state.get_data()

    if ...:
        ...
    else:
        await callback.message.answer(
            "❌ Действие отменено",
            reply_markup=add_only_back_button("← Назад", callback_data="admin:admin")
        )

    await state.clear()


@auxiliary_router.callback_query(F.data.startswith("admin:confirm_"), UserSearch.waiting_for_unban_confirmation)
async def confirm_unban_user(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    action = callback.data.split("_")[1]
    user_data = await state.get_data()

    if ...:
        ...
    else:
        await callback.message.answer(
            "❌ Действие отменено",
            reply_markup=add_only_back_button("← Назад", callback_data="admin:admin")
        )

    await state.clear()


# -------------------SEND USER MESSAGE------------------------------------
@auxiliary_router.callback_query(F.data == "admin:user_mes")
async def start_send_message_to_user(
        callback: CallbackQuery,
        state: FSMContext
):
    """Send a message to user by id or username"""
    await callback.answer()
    user_data = await state.get_data()

    if "user_id" not in user_data:
        await callback.answer("❌ Ошибка: пользователь не найден")
        return

    await callback.message.answer(
        "✉️ Введите текст сообщения для пользователя (макс. 1000 символов):",
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )

    await state.set_state(UserSearch.waiting_for_message)


@auxiliary_router.message(UserSearch.waiting_for_message)
async def send_to_message_to_user(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    user_data = await state.get_data()
    text = message.text

    if len(text) > 1000:
        await message.answer(
            "❌ Сообщение слишком длинное (макс. 1000 символов)",
            reply_markup=add_only_back_button(text="← Назад", callback_data="admin:admin")
        )
        return

    try:
        await bot.send_message(
            chat_id=user_data["user_id"],
            text=text
        )
        await message.answer(
            "✅ Сообщение отправлено пользователю",
            reply_markup=add_only_back_button(text="← Назад", callback_data="admin:admin")
        )
        logger.info(f"Админ {message.from_user.id} отправил сообщение {user_data["user_id"]}")

    except Exception as e:
        logger.error(f"Не получается отправить пользователю сообщение: {e}")
        await message.answer(
            "❌ Не удалось отправить сообщение",
            reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
        )
    finally:
        await state.clear()


# ---------------------------User Stats------------------------------------
@auxiliary_router.callback_query(F.data == "admin:user_stats")
async def request_user_stats(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    """Statistic on user"""
    await callback.answer()
    user_data = await state.get_data()

    # Здесь вы будете реализовывать фактическое получение статистики.
    # Например:
    # stats = await get_user_stats(session, user_data["user_id"])

    stats_text = (
        f"📊 Статистика пользователя @{user_data['username']} за последнюю неделю:\n\n"
        f"Отправлено команд: \n"
        f"Активность: \n"
        f"Последний визит: "
    )

    await callback.message.answer(
        stats_text,
        reply_markup=add_only_back_button(text="← Отмена", callback_data="admin:admin")
    )
