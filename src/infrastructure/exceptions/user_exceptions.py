from fastapi import status

from infrastructure.base_entities.base_exception import BaseAPIException


class ProfileNotFound(BaseAPIException):
    message = "This profile does not exists"
    status_code = status.HTTP_404_NOT_FOUND


class ProfileAlreadyExists(BaseAPIException):
    message = "This profile already exists"
    status_code = status.HTTP_403_FORBIDDEN
