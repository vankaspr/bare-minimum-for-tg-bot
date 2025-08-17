from typing import Optional
from sqlalchemy import select, update, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, BanRecord
from settings.middlewares import logger
from datetime import datetime, timezone


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
        user_id: int,
        ban_reason: str = "Причина не указана",
        banned_by: int | None = None
) -> None:
    """ban user by ID"""
    user = await get_user_by_id(session, user_id)

    #if not user:
    #    raise ValueError("Пользователь не найден")

    user.is_banned = True

    ban_record = BanRecord(
        user_id=user_id,
        ban_reason=ban_reason,
        banned_by=banned_by,
        is_active=True,
        unban_date=None,  # Явно указываем None для новых банов
        unbanned_by=None,
        unban_reason=None
    )

    session.add(ban_record)
    await session.commit()



async def unban_user(
        session: AsyncSession,
        user_id: int,
        unbanned_by: int | None = None,
        unban_reason: str = "Причина не указана",
) -> None:
    """unban user by ID"""
    user = await get_user_by_id(session, user_id)

    #if not user:
    #    raise ValueError("Пользователь не найден")

    user.is_banned = False

    stmt = (
        update(BanRecord)
        .where(
            and_(
                BanRecord.user_id == user_id,
                BanRecord.is_active.is_(True)  # Используем is_() для булевых значений
            )
        )
        .values(
            is_active=False,
            unbanned_by=unbanned_by,
            unban_date=datetime.now(timezone.utc),
            unban_reason=unban_reason
        )
    )

    await session.execute(stmt)
    await session.commit()
