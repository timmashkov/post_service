import logging
from typing import NoReturn

from fastapi import APIRouter, FastAPI

from infrastructure.base_entities.singleton import Singleton


class Server(Singleton):
    def __init__(
        self,
        name: str,
        routers: list[APIRouter] = None,
        start_callbacks: list[callable] = None,
        stop_callbacks: list[callable] = None,
    ) -> NoReturn:
        self.name = name
        self.app = FastAPI(title=name)
        self.routers = routers or []
        self._init_routers()
        self.start_callbacks = start_callbacks or []
        self.stop_callbacks = stop_callbacks or []
        self._init_start_callbacks()
        self._init_stop_callbacks()

    def _init_routers(self):
        for router in self.routers:
            self.app.include_router(router)
        logging.info("Инициализация routers прошла успешно")

    def _init_start_callbacks(self):
        for callback in self.start_callbacks:
            self.app.on_event("startup")(callback)
        logging.info("Инициализация startup callbacks прошла успешно")

    def _init_stop_callbacks(self):
        for callback in self.stop_callbacks:
            self.app.on_event("shutdown")(callback)
        logging.info("Инициализация shutdown callbacks прошла успешно")
