from redis import Redis

from application.container import Container
from domain.post.registry import PostReadRegistry, PostWriteRegistry
from infrastructure.exceptions.user_exceptions import PostNotFound


async def put_likes(
    post_uuid: str,
    post_read: PostReadRegistry = Container.post_read_registry(),
    post_write: PostWriteRegistry = Container.post_write_registry(),
) -> None:
    if existing_post := await post_read.get(post_uuid=post_uuid):
        await post_write.put_like(post_uuid=post_uuid, likes_count=existing_post.likes)
    raise PostNotFound


async def accumulate_data(redis: Redis = Container.redis()):
    data = await redis.g


async def likes_task(post_uuid: str, redis: Redis = Container.redis()):
    await redis.set(name=post_uuid, value=1)
