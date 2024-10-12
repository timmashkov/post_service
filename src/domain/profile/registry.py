from typing import Any, List, Optional, Union
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.profile.schema import CreateProfile
from infrastructure.base_entities.abs_repository import (
    AbstractReadRepository,
    AbstractWriteRepository,
)
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import Friend, Profile
from infrastructure.exceptions.profile_exceptions import ProfileAlreadyExists


class ProfileReadRegistry(AbstractReadRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Profile
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    @classmethod
    def __set_filter(cls, query: select, filters: Any = None) -> select:
        if filters:
            query = filters.filter(query)
        return query

    async def find(
        self,
        filters: Any = None,
    ) -> Union[list, select]:
        query = select(self.model)
        query = self.__set_filter(query, filters)
        async with self.async_session_factory() as session:
            result = await session.execute(query)
            return result.scalars().unique().all()

    async def get(self, prof_uuid: UUID) -> Optional[Profile]:
        async with self.transactional_session() as session:
            stmt = select(self.model).filter(self.model.uuid == prof_uuid)
            result = await session.execute(stmt)
            answer = result.scalar_one_or_none()
        return answer

    async def get_by_user_uuid(self, user_uuid: str) -> Optional[Profile]:
        async with self.transactional_session() as session:
            stmt = select(self.model).filter(self.model.user_uuid == user_uuid)
            result = await session.execute(stmt)
            answer = result.scalar_one_or_none()
        return answer

    async def get_list(
        self,
        parameter: Any = "created_at",
    ) -> Optional[List[Profile]]:
        async with self.async_session_factory() as session:
            final = None
            if option := getattr(self.model, parameter):
                stmt = select(self.model).order_by(option)
                result = await session.execute(stmt)
                final = result.scalars().all()
        return final

    async def check_existing_friend(
        self, profile_uuid: UUID, friend_uuid: UUID
    ) -> Optional[Friend]:
        async with self.async_session_factory() as session:
            existing_friend = (
                select(Friend)
                .where(Friend.profile_id == profile_uuid)
                .where(Friend.friend_id == friend_uuid)
            )
            result = await session.execute(existing_friend)
            return result.scalar_one_or_none()


class ProfileWriteRegistry(AbstractWriteRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Profile
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def create(self, cmd: CreateProfile) -> Optional[Profile]:
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
            raise ProfileAlreadyExists

    async def update(
        self,
        cmd: CreateProfile,
        prof_uuid: UUID,
    ) -> Optional[Profile]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .values(**cmd.model_dump())
                .where(self.model.uuid == prof_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer

    async def delete(self, prof_uuid: UUID) -> Optional[Profile]:
        async with self.transactional_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.uuid == prof_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer

    async def add_friend(self, profile_uuid: UUID, friend_uuid: UUID) -> Friend:
        async with self.transactional_session() as session:
            stmt = insert(Friend).values(
                profile_uuid=profile_uuid, friend_uuid=friend_uuid
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer
