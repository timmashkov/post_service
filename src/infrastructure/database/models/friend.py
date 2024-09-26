from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base


class Friend(Base):
    __table_args__ = (
        UniqueConstraint("profile_id", "friend_id", name="idx_unique_profile_friend"),
        {"extend_existing": True},
    )

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profiles.uuid"))
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("profiles.uuid"))
