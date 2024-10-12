from typing import Any, List, Optional, Union
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.post.schema import CreatePost
from infrastructure.base_entities.abs_repository import (
    AbstractReadRepository,
    AbstractWriteRepository,
)
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import Post
from infrastructure.exceptions.profile_exceptions import PostAlreadyExists


class PostReadRegistry(AbstractReadRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Post
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def get(self, post_uuid: Union[UUID, str]) -> Optional[Post]:
        async with self.async_session_factory() as session:
            stmt = select(self.model).filter(self.model.uuid == post_uuid)
            result = await session.execute(stmt)
            answer = result.scalar_one_or_none()
        return answer

    async def get_list(
        self,
        parameter: Any = "created_at",
    ) -> Optional[List[Post]]:
        async with self.async_session_factory() as session:
            final = None
            if option := getattr(self.model, parameter):
                stmt = select(self.model).order_by(option)
                result = await session.execute(stmt)
                final = result.scalars().all()
        return final


class PostWriteRegistry(AbstractWriteRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Post
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def create(self, cmd: CreatePost) -> Optional[Post]:
        try:
            async with self.transactional_session() as session:
                stmt = (
                    insert(self.model).values(**cmd.model_dump()).returning(self.model)
                )
                result = await session.execute(stmt)
                await session.commit()
                answer = result.scalar_one_or_none()
            return answer
        except (UniqueViolationError, IntegrityError):
            raise PostAlreadyExists

    async def update(
        self,
        cmd: CreatePost,
        post_uuid: UUID,
    ) -> Optional[Post]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .values(**cmd.model_dump())
                .where(self.model.uuid == post_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer

    async def delete(self, post_uuid: UUID) -> Optional[Post]:
        async with self.transactional_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.uuid == post_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer

    async def put_like(self, post_uuid: str | UUID, likes_count: int) -> Optional[dict]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.uuid == post_uuid)
                .values(likes=likes_count)
                .returning(self.model.likes)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.mappings().first()
        return answer
