from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from infrastructure.base_entities.base_filter import PatchedFilter
from infrastructure.database.models import Post


class GetPostByUUID(BaseModel):
    uuid: UUID


class CreatePost(BaseModel):
    header: str
    hashtag: str
    body: str
    likes: Optional[int] = None
    profile_id: UUID

    @field_validator("hashtag")
    def check_hashtag(cls, data):
        if data.startswith("#"):
            return data
        raise ValueError("Hashtag must starts with '#'")


class PostReturnData(GetPostByUUID, CreatePost):
    created_at: datetime
    updated_at: datetime


class ProfileFilter(PatchedFilter):
    uuid: Optional[UUID] = None
    header: Optional[str] = None
    hashtag: Optional[str] = None
    body: Optional[str] = None
    likes: Optional[str] = None

    profile_id: Optional[UUID] = None

    class Constants(PatchedFilter.Constants):
        model = Post
