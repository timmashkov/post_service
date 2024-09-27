import asyncio
import logging
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
