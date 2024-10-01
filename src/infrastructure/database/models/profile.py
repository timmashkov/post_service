from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from .post import Post


class Profile(Base):
    user_uuid: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, comment="УУИД юзера"
    )
    first_name: Mapped[str] = mapped_column(
        String(20), unique=False, nullable=False, default=""
    )
    last_name: Mapped[str] = mapped_column(
        String(30), unique=False, nullable=False, default=""
    )
    occupation: Mapped[str] = mapped_column(String(30), unique=False, nullable=True)
    status: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    bio: Mapped[str] = mapped_column(Text, unique=False, nullable=True)

    file_uuid: Mapped[str] = mapped_column(
        String, unique=True, nullable=True, comment="УУИД фото"
    )

    friends: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary="friends",
        primaryjoin="Profile.uuid==Friend.profile_id",
        secondaryjoin="Profile.uuid==Friend.friend_id",
        lazy="noload",
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
    )
