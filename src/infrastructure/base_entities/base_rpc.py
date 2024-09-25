from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop, Future
from typing import Any, Awaitable, Callable, Union
from uuid import UUID


class BaseRPC(ABC):
    _futures: dict[Union[UUID, str] : Union[Future, AbstractEventLoop]] = {}

    @staticmethod
    async def cancel_consumer(queue, consumers):
        for key, val in consumers.items():
            await queue.cancel(key)

    @abstractmethod
    async def on_response(self, message: Any) -> None:
        pass

    @abstractmethod
    async def call(self, queue_name: str, **kwargs) -> Any:
        pass

    @abstractmethod
    async def consume_queue(
        self,
        func: Union[Callable, Awaitable],
        queue_name: str,
    ) -> None:
        pass

    @abstractmethod
    async def on_call_message(self, exchange, func, message: Any) -> None:
        pass
