from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BanRecord
from database.models import User
from settings.middlewares import logger


async def get_or_create_user(
        session: AsyncSession,
        telegram_user
) -> User:

    result = await session.execute(
        select(User).where(User.id == telegram_user.id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            id=telegram_user.id,
            username=telegram_user.username,
            is_banned=False
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_user_by_id(
        session: AsyncSession,
        user_id: int
) -> Optional[User]:

    try:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Проблемы с нахождением этого бублика {user_id}: {e}")
        return None


async def get_user_by_username(
        session: AsyncSession,
        username: str
) -> Optional[User]:

    try:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Проблемы с нахождением этого бублика {username}: {e}")
        return None

async def ban_user(
        session: AsyncSession,
        user_id: int,
        admin_id: int,
        reason: str
) -> tuple[bool, str]:

    try:

        user: User = await get_user_by_id(session, user_id)

        if not user:
            return False, "Пользователь не найден"

        user.is_banned = True
        ban = BanRecord(
            user_id=user_id,
            reason=reason,
            banned_by=admin_id
        )
        session.add(ban)
        await session.commit()
        return True, f"Пользователь {user_id} забанен"

    except SQLAlchemyError as e:
        logger.error(f"Проблемы с баном для этого бублика {user_id}")
        await session.rollback()
        return False, f"Ошибка бана: {str(e)}"