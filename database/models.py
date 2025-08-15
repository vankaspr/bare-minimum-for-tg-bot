from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    is_banned = Column(Boolean)
    join_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    #last_activity = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                           #onupdate=lambda: datetime.now(timezone.utc))

    activities = relationship(
        "UserActivity",
        back_populates="user"
    )

    bans = relationship(
        "BanRecord",
        back_populates="user"
    )


class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True,  autoincrement=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    action =  Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user =  relationship(
        "User",
        back_populates="activities"
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
