from typing import Optional

from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Sightseeing(Base):
    __tablename__ = "sightseeings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    location: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
