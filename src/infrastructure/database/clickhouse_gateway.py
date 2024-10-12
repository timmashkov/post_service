from asynch import connect


class ClickHouseManager:
    def __init__(
        self, host: str, port: int, database: str, user: str, password: str
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    async def __get_connection(self):
        return await connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )

    async def execute(self, query: str, params=None) -> None:
        conn = await self.__get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            await conn.commit()

    async def fetch_one(self, query: str, params=None):
        conn = await self.__get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()

    async def fetch_all(self, query: str, params=None):
        conn = await self.__get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

    async def create(self, table: str, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join([f"%({key})s" for key in data.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        await self.execute(query, data)

    async def get(self, table: str, search_params: dict):
        where_clause = " AND ".join(
            [f"{key} = %({key})s" for key in search_params.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
        return await self.fetch_one(query, search_params)

    async def get_list(self, table: str, search_params: dict = None):
        if search_params:
            where_clause = " AND ".join(
                [f"{key} = %({key})s" for key in search_params.keys()]
            )
            query = f"SELECT * FROM {table} WHERE {where_clause}"
        else:
            query = f"SELECT * FROM {table}"
        return await self.fetch_all(query, search_params)

    async def update(self, table: str, update_data: dict, search_params: dict):
        set_clause = ", ".join([f"{key} = %({key})s" for key in update_data.keys()])
        where_clause = " AND ".join(
            [f"{key} = %({key})s" for key in search_params.keys()]
        )
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        data = {**update_data, **search_params}
        await self.execute(query, data)

    async def delete(self, table: str, search_params: dict):
        where_clause = " AND ".join(
            [f"{key} = %({key})s" for key in search_params.keys()]
        )
        query = f"DELETE FROM {table} WHERE {where_clause}"
        await self.execute(query, search_params)

    async def create_table(self, table_name: str, columns: dict) -> None:
        columns_definition = ", ".join(
            [f"{col_name} {col_type}" for col_name, col_type in columns.items()]
        )
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition}) ENGINE = MergeTree() ORDER BY tuple()"
        await self.execute(query)
