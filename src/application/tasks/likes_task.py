from asyncio import Queue

from redis import Redis

from application.config import settings
from application.container import Container
from domain.post.registry import PostReadRegistry, PostWriteRegistry
from infrastructure.exceptions.profile_exceptions import PostNotFound


async def put_likes(
    post_uuid: str,
    post_read: PostReadRegistry = Container.post_read_registry(),
    post_write: PostWriteRegistry = Container.post_write_registry(),
) -> None:
    if existing_post := await post_read.get(post_uuid=post_uuid):
        await post_write.put_like(post_uuid=post_uuid, likes_count=existing_post.likes)
    raise PostNotFound


async def accumulate_data(redis: Redis = Container.redis()):
    likes_queue = Queue(maxsize=settings.LIKES_COUNT)
    data = await redis.g


async def likes_task(post_uuid: str, redis: Redis = Container.redis()):
    await redis.set(name=post_uuid, value=1)
