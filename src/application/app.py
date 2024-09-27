from application.amqp_handler import process
from application.config import settings
from application.container import Container
from infrastructure.server.server import Server
from presentation.post import PostRouter
from presentation.profile import ProfileRouter

post_service = Server(
    name=settings.NAME,
    routers=[ProfileRouter.api_router, PostRouter.api_router],
    start_callbacks=[
        process.start,
        # Container.producer_client().connect
    ],
    stop_callbacks=[
        Container.redis().close,
        process.close,
        Container.producer_client().disconnect,
        Container.consumer_client().disconnect,
    ],
).app
