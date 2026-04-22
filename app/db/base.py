from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Optional, Any


class DatabasePool(ABC):
    _pool: Optional[Any] = None

    @classmethod
    @abstractmethod
    async def get_pool(cls) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def close(cls):
        pass

    @classmethod
    @asynccontextmanager
    async def connection(cls):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                yield cursor

    @classmethod
    async def execute_query(cls, sql: str) -> list[dict]:
        async with cls.connection() as cursor:
            await cursor.execute(sql)
            result = await cursor.fetchall()
            return result if result else []
