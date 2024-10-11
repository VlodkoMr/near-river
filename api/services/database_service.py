from tortoise import Tortoise
from config.settings import conf


class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    async def connect(self):
        await Tortoise.init(
            db_url=conf.DB_CONNECTION,
            modules={'models': conf.MODELS_LIST}
        )
        await Tortoise.generate_schemas()

    async def close(self):
        await Tortoise.close_connections()

    async def init(self):
        await self.connect()

    @classmethod
    async def initialize(cls):
        service = cls()
        await service.init()
        return service

    @classmethod
    async def shutdown(cls):
        service = cls()
        await service.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def run_raw_sql(self, query: str, *args):
        """
        Execute a raw SQL query and return the result.
        :param query: The raw SQL query string
        :param args: Optional parameters for the query
        :return: The query result
        """
        connection = Tortoise.get_connection('default')  # Default connection name
        result = await connection.execute_query(query, *args)
        return result[1] if len(result) == 2 else result[0]
