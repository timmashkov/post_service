import asyncio
from multiprocessing import Process

from application.config import settings
from application.container import Container
from infrastructure.broker.kafka import KafkaConsumer
from infrastructure.handlers.account_handler import create_profile_on_message


async def _amqp_handler(
    kafka_client: KafkaConsumer = Container.consumer_client(),
) -> None:
    await kafka_client.connect(topic_name=settings.KAFKA.topics.register_topic)
    await kafka_client.init_consuming(create_profile_on_message)


def amqp_handler():
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(_amqp_handler())
    _loop.run_forever()


process = Process(target=amqp_handler)
