import asyncio
import logging
from asyncio import Semaphore, gather
from typing import Any, Coroutine

import redis


async def run_with_timeout(
    coro: Coroutine[Any, Any, Any],
    timeout: int | float,
    operation_name: str = "Имя операции не указано",
    logger: logging.Logger = logging,
) -> Any:
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except (TimeoutError, redis.TimeoutError, asyncio.TimeoutError):
        logger.warning(f"Таймаут ожидания операции {operation_name!r}")
        return None
    except Exception as error:
        logger.error(f"Ошибка выполнения операции {operation_name!r}: {error}")
        return None


async def run_with_semaphore(semaphore: Semaphore, coro):
    async with semaphore:
        return await coro


async def safe_gather(
    *coros_or_futures,
    parallelism_size: int = 10,
    return_exceptions: bool = False,
):
    semaphore = Semaphore(value=parallelism_size)
    coroutines = [run_with_semaphore(semaphore, task) for task in coros_or_futures]
    return await gather(*coroutines, return_exceptions=return_exceptions)
