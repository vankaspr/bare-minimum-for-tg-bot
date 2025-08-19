from datetime import datetime
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from core.middlewares import logger


class BannedUserFilter(BaseFilter):
    """A filter to check if a user is banned."""

    async def __call__(
        self, update: Union[Message, CallbackQuery], session: AsyncSession
    ) -> bool:

        user = update.from_user
        db_user = await session.get(User, user.id)

        if not db_user:
            db_user = User(
                id=user.id,
                username=user.username,
                is_banned=False,
                join_date=datetime.now(),
            )
            session.add(db_user)
            await session.commit()
            logger.info(
                f"Добавлен новый пользователь {user.id} ({user.username}) в базу"
            )

        if db_user.is_banned:
            logger.warning(
                f"Забаненный пользователь {user.id} ({user.username}) пытался использовать бота"
            )
            if isinstance(update, CallbackQuery):
                await update.answer(
                    "🚫 Вы забанены и не можете использовать бота", show_alert=True
                )
            else:
                await update.answer("⚠️ Вы забанены и не можете использовать бота")
            return False
        return True
