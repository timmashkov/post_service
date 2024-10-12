from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from infrastructure.base_entities.base_filter import PatchedFilter
from infrastructure.database.models import Profile


class GetProfileByUUID(BaseModel):
    uuid: UUID


class CreateProfile(BaseModel):
    user_uuid: str
    first_name: str
    last_name: str
    occupation: Optional[str] = None
    status: Optional[str] = None
    bio: Optional[str] = None
    file_uuid: Optional[str] = None


class ProfileReturnData(GetProfileByUUID, CreateProfile):
    created_at: datetime
    updated_at: datetime


class ProfileFilter(PatchedFilter):
    uuid: Optional[UUID] = None
    user_uuid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None
    status: Optional[str] = None
    bio: Optional[str] = None
    file_uuid: Optional[str] = None

    class Constants(PatchedFilter.Constants):
        model = Profile
