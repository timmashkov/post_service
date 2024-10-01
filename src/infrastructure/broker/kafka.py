import logging
from asyncio import AbstractEventLoop, get_event_loop
from typing import Awaitable, List, Optional, Union

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from infrastructure.base_entities.base_mq import BaseMQ


class KafkaProducer(BaseMQ):
    def __init__(
        self,
        host: str,
        port: int,
        loop: Optional[AbstractEventLoop] = None,
        topics: Optional[List[str]] = [],
        logging_config: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.loop = loop if loop else get_event_loop()
        self.topics = topics if topics else []
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=f"{host}:{port}",
            loop=self.loop,
        )

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")

    async def connect(self) -> None:
        await self._init_logger()
        await self.__producer.start()
        logging.info("Инициализация kafka прошла успешно")

    async def disconnect(self) -> None:
        await self._init_logger()
        await self.__producer.stop()
        logging.info("Отключение kafka прошла успешно")

    async def send_message(
        self,
        message: Union[str, bytes, list, dict],
    ):
        await self._init_logger()
        for topic in self.topics:
            await self.__producer.send_and_wait(
                topic=topic,
                value=self.serialize_message(message),
            )
            logging.info("Сообщение отправлено")


class KafkaConsumer(BaseMQ):
    def __init__(
        self,
        host: str,
        port: int,
        loop: Optional[AbstractEventLoop] = None,
        topics: Optional[List[str]] = [],
        logging_config: Optional[str] = None,
    ):
        self.host = host
        self.port = port
        self.loop = loop if loop else get_event_loop()
        self.topics = topics if topics else []
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self.__consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=f"{host}:{port}",
            loop=self.loop,
        )

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")

    async def connect(self, topic_name: Optional[str] = None) -> None:
        await self._init_logger()
        await self.__consumer.start()
        self.choose_topic(topic=topic_name)
        logging.info("Инициализация kafka прошла успешно")

    async def disconnect(self) -> None:
        await self._init_logger()
        await self.__consumer.stop()
        logging.info("Отключение kafka прошла успешно")

    async def init_consuming(self, on_message: callable | Awaitable) -> None:
        await self._init_logger()
        async for msg in self.__consumer:
            response = self.deserialize_message(msg.value)
            await on_message(response)
            logging.info("Сообщение получено")

    def choose_topic(self, topic: Optional[str]) -> None:
        if topic:
            routing_keys: Optional[list[str]] = []
            routing_keys.append(topic)
            if routing_keys:  # Убедимся, что список не пустой
                self.__consumer.subscribe(topics=routing_keys)
            else:
                raise ValueError(f"Топик {topic} не найден в списке доступных топиков")
        else:
            raise ValueError("Необходимо указать топик")
