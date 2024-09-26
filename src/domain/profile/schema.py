from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GetProfileByUUID(BaseModel):
    uuid: UUID


class CreateProfile(BaseModel):
    user_uuid: str
    first_name: str
    last_name: str
    occupation: Optional[str] = None
    status: Optional[str] = None
    bio: Optional[str] = None


class ProfileReturnData(GetProfileByUUID, CreateProfile):
    created_at: datetime
    updated_at: datetime
