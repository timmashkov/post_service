import asyncio
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel

from domain.profile.schema import CreateProfile, GetProfileByUUID, ProfileReturnData
from service.profile_service import ProfileService


class ProfileRouter:
    api_router = APIRouter(prefix="/profile", tags=["Profile"])
    output_model: BaseModel = ProfileReturnData
    input_model: BaseModel = CreateProfile
    service_client: ProfileService = Depends(ProfileService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def get(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.get(cmd=GetProfileByUUID(uuid=user_uuid))

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
        data: Optional[UploadFile] = None,
        service=service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, prof_uuid=GetProfileByUUID(uuid=user_uuid), avatar=data
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        user_uuid: str | UUID,
        service=service_client,
    ) -> output_model:
        return await service.delete(prof_uuid=GetProfileByUUID(uuid=user_uuid))
