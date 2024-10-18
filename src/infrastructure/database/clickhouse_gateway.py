import logging

from clickhouse_driver import Client
from pypika import Query, Table

from application.config import settings
from infrastructure.database.models import Base
from infrastructure.handlers.asyncio_handlers import run_in_executor


class ClickHouseManager:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        logger: logging.Logger = logging,
    ) -> None:
        logging.basicConfig(level=logging.INFO)
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.logger = logger
        self.client = Client(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self._options = settings.CLICKHOUSE.TYPES

    @property
    def clickhouse_types(self) -> dict:
        return dict(self._options)

    async def select_object(self, table: str, search_params: dict, **kwargs):
        where_clause = " AND ".join(
            [f"{key} = %(key)s" for key in search_params.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
        return await run_in_executor(
            func=self.client.execute,
            query=query,
            **kwargs,
        )

    async def select_object_list(self, table: str, search_params: dict = None):
        t = Table(table)
        query = Query.from_(t).select("*")

        if search_params:
            for key, value in search_params.items():
                query = query.where(t[key] == value)

        query_str = str(query)
        return await run_in_executor(
            func=self.client.execute,
            query=query_str,
        )

    async def insert_object(self, table: str, data: dict):
        t = Table(table)
        query = Query.into(t).columns(*data.keys()).insert(*data.values())
        query_str = str(query)
        return await run_in_executor(
            func=self.client.execute,
            query=query_str,
        )

    async def update_object(self, table: str, update_data: dict, search_params: dict):
        t = Table(table)
        query = Query.update(t)

        for key, value in update_data.items():
            query = query.set(t[key], value)

        for key, value in search_params.items():
            query = query.where(t[key] == value)

        query_str = str(query)
        return await run_in_executor(
            func=self.client.execute,
            query=query_str,
        )

    async def delete_object(self, table: str, search_params: dict):
        t = Table(table)
        query = Query.from_(t).delete()

        for key, value in search_params.items():
            query = query.where(t[key] == value)

        query_str = str(query)
        return await run_in_executor(
            func=self.client.execute,
            query=query_str,
        )

    async def __create_table(self, table_name: str, columns: dict, **kwargs) -> None:
        self.logger.info(f"Инициализация создания таблицы {table_name}")
        columns_definition = ", ".join(
            [f"{col_name} {col_type}" for col_name, col_type in columns.items()]
        )
        query = f"""
                CREATE TABLE IF NOT EXISTS 
                {self.database}.{table_name} 
                ({columns_definition}) 
                ENGINE = MergeTree ORDER BY uuid
                """
        await run_in_executor(
            func=self.client.execute,
            query=query,
            **kwargs,
        )
        self.logger.info(f"Таблицы {table_name} успешно создана")

    async def create_table(self, model: Base) -> None:
        table_name = model.__tablename__
        columns = {}
        for column in model.__table__.columns:
            column_name = column.name
            column_type = str(column.type)
            columns[column_name] = self.clickhouse_types[column_type]
        await self.__create_table(table_name, columns)

    async def get_tables(self, **kwargs) -> list:
        query = f"SHOW TABLES FROM {self.database}"
        return await run_in_executor(
            func=self.client.execute,
            query=query,
            **kwargs,
        )
