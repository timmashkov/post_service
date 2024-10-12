import asyncio
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi_filter import FilterDepends
from pydantic import BaseModel

from domain.profile.schema import (
    CreateProfile,
    GetProfileByUUID,
    ProfileFilter,
    ProfileReturnData,
)
from service.profile_service import ProfileReadService, ProfileWriteService


class ProfileRouter:
    api_router = APIRouter(prefix="/profile", tags=["Profile"])
    output_model: BaseModel = ProfileReturnData
    input_model: BaseModel = CreateProfile
    filters: ProfileFilter = FilterDepends(ProfileFilter)
    read_service_client: ProfileReadService = Depends(ProfileReadService)
    write_service_client: ProfileWriteService = Depends(ProfileWriteService)

    @staticmethod
    @api_router.get("/one", response_model=output_model)
    async def get(
        user_uuid: str | UUID,
        service=read_service_client,
    ) -> output_model:
        return await service.get(cmd=GetProfileByUUID(uuid=user_uuid))

    @staticmethod
    @api_router.get("/find", response_model=List[output_model])
    async def find(
        filters=filters,
        service=read_service_client,
    ) -> output_model:
        return await service.find(filters=filters)

    @staticmethod
    @api_router.get("/all", response_model=List[output_model])
    async def get_list(
        parameter: str = "created_at",
        service=read_service_client,
    ) -> List[output_model]:
        return await service.get_list(parameter=parameter)

    @staticmethod
    @api_router.post("/create", response_model=output_model)
    async def create(
        incoming_data: input_model,
        service=write_service_client,
    ) -> output_model:
        return await service.create(data=incoming_data)

    @staticmethod
    @api_router.patch("/update{user_uuid}", response_model=output_model)
    async def update(
        user_uuid: str | UUID,
        incoming_data: input_model,
        data: Optional[UploadFile] = None,
        service=write_service_client,
    ) -> output_model:
        return await service.update(
            data=incoming_data, prof_uuid=GetProfileByUUID(uuid=user_uuid), avatar=data
        )

    @staticmethod
    @api_router.delete("/delete", response_model=output_model)
    async def delete(
        user_uuid: str | UUID,
        service=write_service_client,
    ) -> output_model:
        return await service.delete(prof_uuid=GetProfileByUUID(uuid=user_uuid))
