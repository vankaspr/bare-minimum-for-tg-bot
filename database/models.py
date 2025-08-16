from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    is_banned = Column(Boolean)
    join_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    bans = relationship(
        "BanRecord",
        back_populates="user"
    )


class BanRecord(Base):
    __tablename__ = "bans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(String(200))
    banned_by = Column(Integer)
    ban_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    user = relationship(
        "User",
        back_populates="bans"
    )
