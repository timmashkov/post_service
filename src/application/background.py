from asyncio import run
from multiprocessing import Process

from application.config import settings
from application.tasks.clickhouse_table_creation import create_tables_task
from infrastructure.handlers.asyncio_handlers import safe_gather, start_task


async def _start_background_tasks():
    tasks = [start_task(create_tables_task(), settings.REPEAT_TIMEOUT)]
    await safe_gather(*tasks)


def start_background_tasks():
    run(_start_background_tasks())


background_process = Process(target=start_background_tasks)
