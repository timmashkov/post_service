import asyncio
from typing import Any, List, Optional
from uuid import UUID

from fastapi import Depends, UploadFile

from application.config import settings
from application.container import Container
from domain.profile.registry import ProfileReadRegistry, ProfileWriteRegistry
from domain.profile.schema import CreateProfile, GetProfileByUUID, ProfileReturnData
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.exceptions.profile_exceptions import FriendAlreadyExist


class ProfileReadService:
    def __init__(
        self,
        read_repository: ProfileReadRegistry = Depends(Container.profile_read_registry),
        cache_repository: RedisCache = Depends(Container.redis_cache),
    ):
        self.read_repo = read_repository
        self.cache = cache_repository

    async def get(self, cmd: GetProfileByUUID) -> Optional[ProfileReturnData]:
        profile = await self.cache.cache(
            ttl=660, timeout=0.1, func=self.read_repo.get, prof_uuid=cmd.uuid
        )
        return profile

    async def get_list(self, parameter: str) -> Optional[List[ProfileReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def find(self, filters: Any = None):
        return await self.read_repo.find(filters=filters)


class ProfileWriteService:
    def __init__(
        self,
        read_repository: ProfileReadRegistry = Depends(Container.profile_read_registry),
        write_repository: ProfileWriteRegistry = Depends(
            Container.profile_write_registry,
        ),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository

    async def create(self, data: CreateProfile) -> Optional[ProfileReturnData]:
        return await self.write_repo.create(cmd=data)

    async def update(
        self,
        data: CreateProfile,
        prof_uuid: GetProfileByUUID,
        avatar: Optional[UploadFile] = None,
    ) -> Optional[ProfileReturnData]:
        asyncio.create_task(
            self.kafka_repo.send_message(
                message=avatar.file,
                topic=settings.KAFKA.topics.media_topic,
            ),
        )
        return await self.write_repo.update(cmd=data, prof_uuid=prof_uuid.uuid)

    async def delete(self, prof_uuid: GetProfileByUUID) -> Optional[ProfileReturnData]:
        return await self.write_repo.delete(prof_uuid=prof_uuid.uuid)

    async def make_friend(self, profile_uuid: UUID, friend_uuid: UUID):
        if await self.read_repo.check_existing_friend(
            profile_uuid=profile_uuid, friend_uuid=friend_uuid
        ):
            raise FriendAlreadyExist
        return await self.write_repo.add_friend(
            profile_uuid=profile_uuid, friend_uuid=friend_uuid
        )
