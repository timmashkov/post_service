from typing import List, Optional

from fastapi import Depends

from application.container import Container
from domain.post.registry import PostReadRegistry, PostWriteRegistry
from domain.post.schema import CreatePost, GetPostByUUID, PostReturnData
from infrastructure.exceptions.profile_exceptions import PostNotFound


class PostReadService:
    def __init__(
        self,
        read_repository: PostReadRegistry = Depends(Container.post_read_registry),
    ):
        self.read_repo = read_repository

    async def get(self, cmd: GetPostByUUID) -> Optional[PostReturnData]:
        return await self.read_repo.get(post_uuid=cmd.uuid)

    async def get_list(self, parameter: str) -> Optional[List[PostReturnData]]:
        return await self.read_repo.get_list(parameter=parameter)


class PostWriteService:
    def __init__(
        self,
        write_repository: PostWriteRegistry = Depends(
            Container.post_write_registry,
        ),
    ):
        self.write_repo = write_repository

    async def create(self, data: CreatePost) -> Optional[PostReturnData]:
        return await self.write_repo.create(cmd=data)

    async def update(
        self, data: CreatePost, post_uuid: GetPostByUUID
    ) -> Optional[PostReturnData]:
        return await self.write_repo.update(cmd=data, post_uuid=post_uuid.uuid)

    async def delete(self, post_uuid: GetPostByUUID) -> Optional[PostReturnData]:
        return await self.write_repo.delete(post_uuid=post_uuid.uuid)
