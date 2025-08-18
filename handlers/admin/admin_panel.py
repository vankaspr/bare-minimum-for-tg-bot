"""
Handler for command --> /admin ✅
Handler for callback --> admin:admin ✅
Handler for callback --> admin:users ✅
                            --> admin:active_ban ✅
                            --> admin:active_ban_list ✅
                            --> admin:found_user ✅
                                --> admin:user_ban ✅
                                --> admin:user_unban ✅
                                --> admin:user_mes ✅
Handler for callback --> admin:error_logs ✅
Handler for callback --> admin:payments
Handler for callback --> admin:broadcast
"""

import html
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import (
    get_active_ban_count,
    get_active_bans_list,
    get_all_active_user_ids,
)
from filters.is_admin import AdminFilter
from keyboards import admin_kb, users_kb
from keyboards.admin_keyboard import search_user_kb, confirm_broadcast_kb
from services import BACK_BUTTON, add_back_to_admin_button
from services.broadcast import broadcast_message_to_users
from services.format_ban import format_ban_list
from middlewares import logger
from config import admin
from utilities.error_logs import get_error_logs

admin_router = Router()
admin_router.callback_query.filter(AdminFilter(admin))


# --- Главное меню ---
@admin_router.callback_query(F.data == "admin:admin")
@admin_router.message(F.text == "/admin")
async def admin(update: Message | CallbackQuery):
    """Get admin keyboards"""
    if isinstance(update, CallbackQuery):
        logger.info("Получении админ-панели с колбэка")
        await update.answer()
        message = update.message
    else:
        logger.info("Получении админ-панели с команды")
        message = update

    await message.answer("Админ-панель ⛏️", reply_markup=admin_kb())


# --- Раздел пользователей ---
@admin_router.callback_query(F.data == "admin:users")
async def get_admin_users(callback: CallbackQuery):
    await callback.answer()
    logger.info("Получении раздела о пользователях с колбэка")
    await callback.message.answer(
        "🛠 Управление пользователями", reply_markup=users_kb()
    )


@admin_router.callback_query(F.data == "admin:found_user")
async def found_user(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🔍 Выберите способ поиска:", reply_markup=search_user_kb()
    )


@admin_router.callback_query(F.data == "admin:active_ban")
async def get_active_ban(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    ban_count = await get_active_ban_count(session)

    list_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Посмотреть список банов",
                    callback_data="admin:active_ban_list",
                )
            ]
        ]
    )
    await callback.message.answer(
        f"🔢 Активных банов: <b>{ban_count}</b>\n",
        parse_mode="HTML",
        reply_markup=add_back_to_admin_button(list_button),
    )


@admin_router.callback_query(F.data == "admin:active_ban_list")
async def show_first_ban_page(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    ban_list = await get_active_bans_list(session)

    await callback.message.answer(format_ban_list(ban_list), reply_markup=BACK_BUTTON)


# --- Системные функции ---
@admin_router.callback_query(F.data == "admin:error_logs")
async def get_admin_logs(callback: CallbackQuery):
    await callback.answer("⏳ Загружаю логи...")

    logs = await get_error_logs()

    if not logs:
        await callback.message.answer(
            "📭 Нет свежих ошибок ERROR/WARNING/DEBUG",
        )

    safe_logs = html.escape(logs)

    await callback.message.answer(
        f"<b>Последние ошибки:</b>\n" f"<pre>{safe_logs}</pre>",
        parse_mode="HTML",
        reply_markup=BACK_BUTTON,
    )


# --- Дополнительные разделы ---
@admin_router.callback_query(F.data == "admin:payments")
async def get_admin_payments(callback: CallbackQuery):
    await callback.answer()
    logger.info("Получении информации о платежах с колбэка")
    await callback.message.answer(
        "Здесь будет лежать инфа о платежах" "На случай если я включу платежи",
    )


class BroadcastStates(StatesGroup):
    waiting_message = State()
    confirmation = State()


@admin_router.callback_query(F.data == "admin:broadcast")
async def get_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📢 Введите сообщение для рассылки:", reply_markup=BACK_BUTTON
    )

    await state.set_state(BroadcastStates.waiting_message)


@admin_router.message(BroadcastStates.waiting_message)
async def process_broadcast_message(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        broadcast_message=message.html_text, message_id=message.message_id
    )

    await message.answer(
        f"Подтвердите рассылку этого сообщения:\n\n{message.html_text}",
        reply_markup=confirm_broadcast_kb(),
        parse_mode="HTML",
    )

    await state.set_state(BroadcastStates.confirmation)


@admin_router.callback_query(
    BroadcastStates.confirmation, F.data == "broadcast:confirm_yes"
)
async def confirm_broadcast(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot
):
    try:
        data = await state.get_data()
        broadcast_message = data.get("broadcast_message")

        users_id = await get_all_active_user_ids(session)
        sent_count, failed_count = await broadcast_message_to_users(
            bot=bot, user_ids=users_id, text=broadcast_message
        )

        await callback.message.edit_text(
            f"📢 Рассылка завершена!\n\n"
            f"✅ Успешно: {sent_count}\n"
            f"❌ Ошибки: {failed_count}",
            reply_markup=BACK_BUTTON,
        )
    except Exception as e:
        logger.error(f"Не удалось разослать рассылку: {e}")
        await callback.message.answer(
            "Что-то пошло не так. Рассылка не удалась", reply_markup=BACK_BUTTON
        )
    finally:
        await state.clear()


@admin_router.callback_query(F.data == "broadcast:cancel")
async def cancel_broadcast(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    await callback.message.edit_text("❌ Рассылка отменена", reply_markup=BACK_BUTTON)
