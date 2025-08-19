from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import admin
from src.core.keyboards.admin_keyboard import users_actions_kb, confirm_kb
from src.database.crud import get_user_by_id, get_user_by_username, bun_user, unban_user
from src.core.filters import AdminFilter
from src.core.services import BACK_BUTTON
from src.core.middlewares import logger


USER_NOT_FOUND_MSG = "❌ Пользователь не найден"


auxiliary_router = Router()
auxiliary_router.callback_query.filter(AdminFilter(admin))
auxiliary_router.message.filter(AdminFilter(admin))


class UserSearch(StatesGroup):
    waiting_for_query = State()
    waiting_for_id = State()
    waiting_for_ban_confirmation = State()
    waiting_for_ban_reason = State()
    waiting_for_unban_confirmation = State()
    waiting_for_unban_reason = State()
    waiting_for_message = State()


# -------------------Found user by ID and Username-----------------------------------
@auxiliary_router.callback_query(F.data == "admin:search_by_id")
async def request_user_by_id(callback: CallbackQuery, state: FSMContext) -> None:
    """Found user by ID"""
    await callback.answer()
    await callback.message.answer("Введите ID пользователя:", reply_markup=BACK_BUTTON)
    await state.set_state(UserSearch.waiting_for_id)


@auxiliary_router.callback_query(F.data == "admin:search_by_username")
async def request_user_by_username(callback: CallbackQuery, state: FSMContext) -> None:
    """Found user by username"""
    await callback.answer()
    await callback.message.answer("Введите username (без @):", reply_markup=BACK_BUTTON)
    await state.set_state(UserSearch.waiting_for_query)


@auxiliary_router.message(UserSearch.waiting_for_id)
async def process_user_id(message: Message, state: FSMContext, session: AsyncSession):
    try:
        user_id = int(message.text.strip())
        user = await get_user_by_id(session, user_id)

        if not user:
            await message.answer(USER_NOT_FOUND_MSG, reply_markup=BACK_BUTTON)
            logger.debug(USER_NOT_FOUND_MSG)
            return

        await state.update_data(user_id=user.id, username=user.username)

        await message.answer(
            f"👤 Найден пользователь:\n\n"
            f"ID: {user.id}\n"
            f"Username: @{user.username}\n"
            f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
            reply_markup=users_actions_kb(),
        )

    except ValueError:
        await message.answer(
            "❌ ID должен быть числом. Попробуйте еще раз:", reply_markup=BACK_BUTTON
        )


@auxiliary_router.message(UserSearch.waiting_for_query)
async def process_username(message: Message, state: FSMContext, session: AsyncSession):
    username = message.text.strip().lstrip("@")

    if not username:
        await message.answer(
            "❌ Username не может быть пустым. Попробуйте еще раз:",
            reply_markup=BACK_BUTTON,
        )
        return

    user = await get_user_by_username(session, username)

    if not user:
        await message.answer(USER_NOT_FOUND_MSG, reply_markup=BACK_BUTTON)
        logger.debug(USER_NOT_FOUND_MSG)
        return

    await state.update_data(user_id=user.id, username=user.username)

    await message.answer(
        f"👤 Найден пользователь:\n\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Статус: {'🔴 Забанен' if user.is_banned else '🟢 Активен'}",
        reply_markup=users_actions_kb(),
    )


# -------------------BAN AND UNBAN USER------------------------------------
@auxiliary_router.callback_query(F.data == "admin:user_ban")
async def request_to_ban_user(callback: CallbackQuery, state: FSMContext):
    """Ban user by ID or Username"""
    await callback.answer()
    data = await state.get_data()
    user_id = data.get("user_id")

    await state.update_data(user_id=user_id)

    await callback.message.answer(
        "📝 Введите причину бана (макс. 200 символов):", reply_markup=BACK_BUTTON
    )

    await state.set_state(UserSearch.waiting_for_ban_reason)


@auxiliary_router.message(UserSearch.waiting_for_ban_reason)
async def process_ban_reason(
    message: Message,
    state: FSMContext,
):
    """Processing the reason for the ban and requesting confirmation"""
    reason = message.text.strip()

    if len(reason) > 200:
        await message.answer(
            "Базар укороти.\n" "Попробуй ещё раз.", reply_markup=BACK_BUTTON
        )
        return

    await state.update_data(ban_reason=reason)
    data = await state.get_data()

    await message.answer(
        f"⚠️ Подтвердите бан пользователя:\n\n"
        f"ID: {data['user_id']}\n"
        f"Причина: {reason}",
        reply_markup=confirm_kb(),
    )

    await state.set_state(UserSearch.waiting_for_ban_confirmation)


@auxiliary_router.callback_query(
    F.data.startswith("admin:confirm_yes"), UserSearch.waiting_for_ban_confirmation
)
async def confirm_ban_user(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot
):
    """Confirmation of ban with recording in BanRecord"""
    data = await state.get_data()
    user_id = data.get("user_id")
    reason = data.get("ban_reason", "Причина не указана")
    admin_id = callback.from_user.id

    try:
        await bun_user(
            session=session, user_id=user_id, ban_reason=reason, banned_by=admin_id
        )

        await callback.message.answer(
            f"✅ Пользователь с ID {user_id} успешно забанен\n" f"Причина: {reason}",
            reply_markup=BACK_BUTTON,
        )

        try:
            await bot.send_message(
                user_id,
                f"⛔ Вы были забанены администратором.\n"
                f"Причина: {reason}\n\n"
                "Для выяснения причин обратитесь к администрации.",
            )
        except Exception as e:
            logger.error(
                f"Не удалось отправить уведомление пользователю {user_id}: {e}"
            )

    except Exception as e:
        logger.error(f"Ошибка при бане пользователя {user_id}: {e}")
        await callback.message.answer(
            f"❌ Не удалось забанить пользователя: {e}", reply_markup=BACK_BUTTON
        )
    finally:
        await state.clear()


@auxiliary_router.callback_query(F.data == "admin:user_unban")
async def request_to_unban_user(callback: CallbackQuery, state: FSMContext):
    """Unban user by ID or Username"""
    await callback.answer()
    data = await state.get_data()
    user_id = data.get("user_id")

    await state.update_data(user_id=user_id)

    await callback.message.answer(
        "📝 Введите причину ан-бана (макс. 200 символов):", reply_markup=BACK_BUTTON
    )

    await state.set_state(UserSearch.waiting_for_unban_reason)


@auxiliary_router.message(UserSearch.waiting_for_unban_reason)
async def process_unban_reason(message: Message, state: FSMContext):
    """Processing the reason for the unban and requesting confirmation"""
    reason = message.text.strip()

    if len(reason) > 200:
        await message.answer(
            "Базар укороти.\n" "Попробуй ещё раз.", reply_markup=BACK_BUTTON
        )
        return

    await state.update_data(unban_reason=reason)
    data = await state.get_data()

    await message.answer(
        f"⚠️ Подтвердите ан-бан пользователя:\n\n"
        f"ID: {data['user_id']}\n"
        f"Причина: {reason}",
        reply_markup=confirm_kb(),
    )

    await state.set_state(UserSearch.waiting_for_unban_confirmation)


@auxiliary_router.callback_query(
    F.data.startswith("admin:confirm_yes"), UserSearch.waiting_for_unban_confirmation
)
async def confirm_unban_user(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot
):
    """Confirmation of unban with recording in BanRecord"""
    data = await state.get_data()
    user_id = data.get("user_id")
    reason = data.get("unban_reason", "Причина не указана")
    admin_id = callback.from_user.id

    try:
        await unban_user(
            session=session, user_id=user_id, unbanned_by=admin_id, unban_reason=reason
        )

        await callback.message.answer(
            f"✅ Пользователь с ID {user_id} успешно разабанен\n" f"Причина: {reason}",
            reply_markup=BACK_BUTTON,
        )

        try:
            await bot.send_message(
                user_id,
                f"✅ Вы были разабанены администратором.\n" f"Причина: {reason}",
            )

        except Exception as e:
            logger.error(
                f"Не удалось отправить уведомление пользователю {user_id}: {e}"
            )

    except Exception as e:
        logger.error(f"Ошибка при ан-бане пользователя {user_id}: {e}")
        await callback.message.answer(
            f"❌ Не удалось ан-банить пользователя: {e}", reply_markup=BACK_BUTTON
        )
    finally:
        await state.clear()


# -------------------SEND USER MESSAGE------------------------------------
@auxiliary_router.callback_query(F.data == "admin:user_mes")
async def start_send_message_to_user(callback: CallbackQuery, state: FSMContext):
    """Send a message to user by id or username"""
    await callback.answer()
    user_data = await state.get_data()

    await callback.message.answer(
        "✉️ Введите текст сообщения для пользователя (макс. 1000 символов):",
        reply_markup=BACK_BUTTON,
    )

    await state.set_state(UserSearch.waiting_for_message)


@auxiliary_router.message(UserSearch.waiting_for_message)
async def send_to_message_to_user(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    text = message.text

    if len(text) > 1000:
        await message.answer(
            "❌ Сообщение слишком длинное (макс. 1000 символов)",
            reply_markup=BACK_BUTTON,
        )
        return

    try:
        await bot.send_message(chat_id=user_data["user_id"], text=text)
        await message.answer(
            "✅ Сообщение отправлено пользователю", reply_markup=BACK_BUTTON
        )
        logger.info(
            f"Админ {message.from_user.id} отправил сообщение {user_data['user_id']}"
        )

    except Exception as e:
        logger.error(f"Не получается отправить пользователю сообщение: {e}")
        await message.answer(
            "❌ Не удалось отправить сообщение", reply_markup=BACK_BUTTON
        )
    finally:
        await state.clear()
