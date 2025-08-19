from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.database.crud import get_user_by_id
from src.core.middlewares import logger


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        user_id = event.from_user.id
        session = data.get("session")

        if not session:
            return await handler(event, data)

        try:
            user = await get_user_by_id(session, user_id)
            if user and user.is_banned:
                if isinstance(event, Message):
                    await event.answer("⛔ Вы забанены и не можете использовать бота")
                elif isinstance(event, CallbackQuery):
                    await event.answer("⛔ Вы забанены", show_alert=True)
                return

        except Exception as e:
            logger.error(f"Ошибка проверки бана: {e}")

        return await handler(event, data)
