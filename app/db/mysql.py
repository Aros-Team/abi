import logging

import aiomysql
from contextlib import asynccontextmanager
from typing import Optional

from app.config import settings
from app.db.base import DatabasePool

logger = logging.getLogger(__name__)


class MySQLPool(DatabasePool):
    _pool: Optional[aiomysql.Pool] = None

    @classmethod
    def _get_connection_params(cls) -> dict:
        if settings.is_production and settings.db_cloud_sql_instance:
            return {
                "unix_socket": f"/cloudsql/{settings.db_cloud_sql_instance}",
                "db": settings.db_name,
            }
        return {
            "host": settings.db_host,
            "port": settings.db_port,
            "db": settings.db_name,
        }

    @classmethod
    async def get_pool(cls) -> aiomysql.Pool:
        if cls._pool is None:
            params = cls._get_connection_params()
            logger.info(f"[DB] Creating connection pool to {settings.db_host}:{settings.db_port}/{settings.db_name}")
            try:
                cls._pool = await aiomysql.create_pool(
                    user=settings.db_user,
                    password=settings.db_password,
                    autocommit=True,
                    minsize=1,
                    maxsize=10,
                    **params,
                )
                logger.info("[DB] Connection pool created successfully")
            except Exception as e:
                logger.error(f"[DB] Failed to create connection pool: {type(e).__name__}: {e}")
                raise
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool is not None:
            logger.info("[DB] Closing connection pool")
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
