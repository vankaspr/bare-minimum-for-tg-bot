from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from settings.middlewares import logger


async def get_or_create_user(
        session: AsyncSession,
        telegram_user
) -> User:
    try:
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
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка при создании пользователя {telegram_user.id}: {e}")
        raise  # Или вернуть None, если это допустимо


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


async def bun_user(
        session: AsyncSession,
        user_id: int
) -> None:
    """ban user by ID"""
    user = await get_user_by_id(session, user_id)
    if user:
        user.is_banned = True
        await session.commit()


async def unban_user(
        session: AsyncSession,
        user_id: int
) -> None:
    """unban user by ID"""
    user = await get_user_by_id(session, user_id)
    if user:
        user.is_banned = False
        await session.commit()
