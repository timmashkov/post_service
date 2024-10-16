from redis.asyncio import Redis

from application.config import settings
from domain.post.registry import PostReadRegistry, PostWriteRegistry
from domain.profile.registry import ProfileReadRegistry, ProfileWriteRegistry
from infrastructure.base_entities.singleton import OnlyContainer, Singleton
from infrastructure.broker.kafka import KafkaConsumer, KafkaProducer
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.clickhouse_gateway import ClickHouseManager


class Container(Singleton):

    redis = OnlyContainer(
        Redis,
        **settings.REDIS,
        decode_responses=True,
    )

    redis_cache = OnlyContainer(RedisCache, redis=redis())

    alchemy_manager = OnlyContainer(
        SessionManager,
        dialect=settings.POSTGRES.dialect,
        host=settings.POSTGRES.host,
        login=settings.POSTGRES.login,
        password=settings.POSTGRES.password,
        port=settings.POSTGRES.port,
        database=settings.POSTGRES.database,
        echo=settings.POSTGRES.echo,
    )

    clickhouse_manager = OnlyContainer(
        ClickHouseManager,
        host=settings.CLICKHOUSE.host,
        user=settings.CLICKHOUSE.user,
        password=settings.CLICKHOUSE.password,
        port=settings.CLICKHOUSE.port,
        database=settings.CLICKHOUSE.database,
    )

    producer_client = OnlyContainer(
        KafkaProducer,
        host=settings.KAFKA.host,
        port=settings.KAFKA.port,
        topics=settings.KAFKA.topics,
        logging_config=settings.LOG_LEVEL,
    )

    consumer_client = OnlyContainer(
        KafkaConsumer,
        host=settings.KAFKA.host,
        port=settings.KAFKA.port,
        topics=settings.KAFKA.topics,
        logging_config=settings.LOG_LEVEL,
    )

    profile_read_registry = OnlyContainer(
        ProfileReadRegistry,
        session_manager=alchemy_manager(),
    )

    profile_write_registry = OnlyContainer(
        ProfileWriteRegistry,
        session_manager=alchemy_manager(),
    )

    post_read_registry = OnlyContainer(
        PostReadRegistry,
        session_manager=alchemy_manager(),
    )

    post_write_registry = OnlyContainer(
        PostWriteRegistry,
        session_manager=alchemy_manager(),
    )
