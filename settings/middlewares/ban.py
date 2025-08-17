from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


from database.crud import get_user_by_id


class BanMiddleware:
    async def __call__(self, handler, event, data):
        # если апдейт вообще не про пользователя — пропускаем
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        user_id = event.from_user.id
        session = data.get("session")

        if session:
            user = await get_user_by_id(session, user_id)
            if user and user.is_banned:
                if isinstance(event, Message):
                    await event.answer("Ты забанен 🚫")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Ты забанен 🚫", show_alert=True)
                return

        return await handler(event, data)
