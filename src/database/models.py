from typing import Optional
from datetime import datetime, timezone

# from sqlalchemy import func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
# from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


""" class User_m2m_sightseeing(Base):
    __tablename__ = "user_m2m_sightseeing"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    sightseeing_id: Mapped[int] = mapped_column(ForeignKey("sightseeings.id", ondelete="CASCADE")) """

""" user_m2m_sightseeing = Table(
    "user_m2m_sightseeing",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("id", Mapped[int], primary_key=True, index=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("sightseeing_id", ForeignKey("sightseeings.id", ondelete="CASCADE"))
) """

class Sightseeing(Base):
    __tablename__ = "sightseeings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))
    location: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    # users: Mapped[List["User"]] = relationship("User", secondary=user_m2m_sightseeing, back_populates="sightseeings")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))
    avatar: Mapped[Optional[str]] = mapped_column(nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(nullable=True)
    # sightseeings: Mapped[List["Sightseeing"]] = relationship("Sightseeing", secondary=user_m2m_sightseeing, back_populates="users")
