import asyncio
import logging

from application.container import Container
from infrastructure.database.clickhouse_gateway import ClickHouseManager
from infrastructure.database.models import Friend, Post, Profile
from infrastructure.handlers.asyncio_handlers import safe_gather


async def create_tables(
    tables: list, clickhouse_client: ClickHouseManager = Container.clickhouse_manager()
) -> None:
    await safe_gather(
        *[clickhouse_client.create_table(model=table) for table in tables]
    )
    logging.info("Таблицы в Clickhouse созданы")


async def create_tables_task() -> asyncio.Task:
    tables = [Profile, Post, Friend]
    logging.info("Инициализация создания таблиц в Clickhouse")
    return asyncio.create_task(create_tables(tables=tables))
