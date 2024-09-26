import logging
from typing import Any, Union
from uuid import UUID

import orjson

from application.container import Container
from infrastructure.database.alchemy_gateway import SessionManager


async def create_profile_on_message(raw_message: Any, session_manager: SessionManager = Container.alchemy_manager()) -> None:
    message = (
        orjson.loads(raw_message.body)
        if isinstance(raw_message.body, (bytes, bytearray))
        else raw_message.body
    )

    if message:
        account_on_message = AccountIn(
            name=message["login"],
            profile_uuid=message["id"],
            profile_phone=message["phone_number"],
        )
        try:
            async with session_manager.async_session_factory() as session:
                existing_account = await find_account_on_message(message["id"])
                if existing_account:
                    if message["event_type"] == EventType.UPDATE:
                        stmt = (
                            update(Account)
                            .values(**account_on_message.model_dump())
                            .where(Account.profile_uuid == message["id"])
                        )
                        await session.execute(stmt)
                        await session.commit()
                    if message["event_type"] == EventType.DELETE:
                        stmt = delete(Account).where(
                            Account.profile_uuid == message["id"],
                        )
                        await session.execute(stmt)
                        await session.commit()
                elif not existing_account and message["event_type"] == EventType.CREATE:
                    stmt = insert(Account).values(**account_on_message.model_dump())
                    await session.execute(stmt)
                    await session.commit()
        except Exception as e:
            logging.error(f"Error while handling event: {e}")


async def find_account_on_message(
        user_uuid: Union[str, UUID],
        session_manager: SessionManager = Container.alchemy_manager(),
) -> AccountOut:
    async with session_manager.async_session_factory() as session:
        stmt = select(Account).where(Account.profile_uuid == user_uuid)
        answer = await session.execute(stmt)
        return answer.scalar_one_or_none()
