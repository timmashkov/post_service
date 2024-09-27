from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from domain.post.schema import CreatePost, GetPostByUUID, PostReturnData
from service.post_service import PostService


class PostRouter:
    api_router = APIRouter(prefix="/post", tags=["Post"])
    output_model: BaseModel = PostReturnData
    input_model: BaseModel = CreatePost
    service_client: PostService = Depends(PostService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def get(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.get(cmd=GetPostByUUID(uuid=user_uuid))

    @staticmethod
    @api_router.get("/all", response_model=List[output_model])
    async def get_list(
        parameter: str = "created_at",
        service=service_client,
    ) -> List[output_model]:
        return await service.get_list(parameter=parameter)

    @staticmethod
    @api_router.post("/create", response_model=output_model)
    async def create(
        incoming_data: input_model,
        service=service_client,
    ) -> output_model:
        return await service.create(data=incoming_data)

    @staticmethod
    @api_router.patch("/update{user_uuid}", response_model=output_model)
    async def update(
        user_uuid: str | UUID,
        incoming_data: input_model,
        service=service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, post_uuid=GetPostByUUID(uuid=user_uuid)
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete(post_uuid=GetPostByUUID(uuid=user_uuid))
