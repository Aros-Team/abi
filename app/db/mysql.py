import aiomysql
from contextlib import asynccontextmanager
from typing import Optional

from app.config import settings


class MySQLPool:
    _pool: Optional[aiomysql.Pool] = None

    @classmethod
    async def get_pool(cls) -> aiomysql.Pool:
        if cls._pool is None:
            cls._pool = await aiomysql.create_pool(
                host=settings.mysql_host,
                port=settings.mysql_port,
                user=settings.mysql_user,
                password=settings.mysql_password,
                db=settings.mysql_database,
                autocommit=True,
                minsize=1,
                maxsize=10,
            )
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool is not None:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None

    @classmethod
    @asynccontextmanager
    async def connection(cls):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                yield cursor


async def execute_query(sql: str) -> list[dict]:
    async with MySQLPool.connection() as cursor:
        await cursor.execute(sql)
        result = await cursor.fetchall()
        return result if result else []
