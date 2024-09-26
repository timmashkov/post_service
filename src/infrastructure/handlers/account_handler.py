from typing import Any

import orjson

from application.container import Container
from domain.profile.registry import ProfileReadRegistry, ProfileWriteRegistry
from domain.profile.schema import CreateProfile


async def create_profile_on_message(raw_message: Any) -> None:
    message = (
        orjson.loads(raw_message)
        if isinstance(raw_message, (bytes, bytearray))
        else raw_message
    )

    await handle_user_data(message=message)


async def handle_user_data(
    message: dict,
    read_profile: ProfileReadRegistry = Container.profile_read_registry(),
    write_profile: ProfileWriteRegistry = Container.profile_write_registry(),
) -> None:
    existing_profile = await read_profile.get_by_user_uuid(
        user_uuid=message["user_uuid"]
    )
    profile_on_message = CreateProfile(
        user_uuid=message["user_uuid"],
        first_name="Иван",
        last_name="Иванов",
        occupation=" ",
        status=" ",
        bio=" ",
    )
    if not existing_profile:
        if message["event_type"] == "create":
            await write_profile.create(cmd=profile_on_message)
    if message["event_type"] == "update":
        await write_profile.update(
            cmd=profile_on_message, prof_uuid=existing_profile.uuid
        )
    if message["event_type"] == "delete":
        await write_profile.delete(prof_uuid=existing_profile.uuid)
