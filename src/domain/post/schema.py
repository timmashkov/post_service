from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class GetPostByUUID(BaseModel):
    uuid: UUID


class CreatePost(BaseModel):
    header: str
    hashtag: str
    body: str
    likes: Optional[str] = None

    @field_validator("hashtag")
    def check_hashtag(cls, data):
        if data.startswith("#"):
            return data
        raise ValueError("Hashtag must starts with '#'")


class PostReturnData(GetPostByUUID, CreatePost):
    created_at: datetime
    updated_at: datetime
