from typing import List, Optional

from fastapi import Depends

from application.container import Container
from domain.profile.registry import ProfileReadRegistry, ProfileWriteRegistry
from domain.profile.schema import CreateProfile, GetProfileByUUID, ProfileReturnData
from infrastructure.cache.redis_cache import RedisCache


class ProfileService:
    def __init__(
        self,
        read_repository: ProfileReadRegistry = Depends(Container.profile_read_registry),
        write_repository: ProfileWriteRegistry = Depends(
            Container.profile_write_registry,
        ),
        cache_repository: RedisCache = Depends(Container.redis_cache),
    ):
        self.read_repo = read_repository
        self.write_repo = write_repository
        self.cache = cache_repository

    async def get(self, cmd: GetProfileByUUID) -> Optional[ProfileReturnData]:
        profile = await self.cache.cache(ttl=660, timeout=0.1, func=self.read_repo.get, prof_uuid=cmd.uuid)
        return profile

    async def get_list(self, parameter: str) -> Optional[List[ProfileReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)

    async def create(self, data: CreateProfile) -> Optional[ProfileReturnData]:
        return await self.write_repo.create(cmd=data)

    async def update(
        self, data: CreateProfile, prof_uuid: GetProfileByUUID
    ) -> Optional[ProfileReturnData]:
        return await self.write_repo.update(cmd=data, prof_uuid=prof_uuid.uuid)

    async def delete(self, prof_uuid: GetProfileByUUID) -> Optional[ProfileReturnData]:
        return await self.write_repo.delete(prof_uuid=prof_uuid.uuid)
