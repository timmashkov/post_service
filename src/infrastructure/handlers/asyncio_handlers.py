import asyncio
import logging
from asyncio import (
    AbstractEventLoop,
    Semaphore,
    gather,
    get_event_loop,
    sleep,
    wait_for,
)
from concurrent.futures import Executor
from functools import partial
from typing import Any, Awaitable, Coroutine, Optional, Union

import redis
from tenacity import retry, wait_random


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


def scheduled_task(
    coro_or_future: callable,
    repeat_timeout: int,
    task_timeout: Optional[float] = None,
    logger: logging.Logger = None,
) -> asyncio.Task:
    logger = logger or logging

    async def repeat():
        while True:
            try:
                await wait_for(coro_or_future, timeout=5)
            except TimeoutError:
                logger.error(
                    f"Task {coro_or_future.__name__} timed out after {task_timeout} seconds."
                )
            except Exception as e:
                raise e
            finally:
                await sleep(repeat_timeout)

    return asyncio.create_task(retry(wait=wait_random(min=1, max=10))(repeat)())


async def run_in_executor(
    func: callable,
    loop: Optional[AbstractEventLoop] = None,
    executor: Optional[Executor] = None,
    *args,
    **kwargs,
) -> Any:
    loop = loop or get_event_loop()
    return await loop.run_in_executor(executor, partial(func, *args, **kwargs))


async def start_task(
    coroutine: Awaitable,
    timeout: Optional[Union[int, float]],
) -> None:
    while True:
        try:
            task = asyncio.create_task(coroutine)
            await task
        except TimeoutError:
            logging.error(f"Task timed out after {30} seconds.")
        finally:
            await sleep(timeout)
