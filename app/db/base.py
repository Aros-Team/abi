from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
import logging
import time
from typing import Optional, Any

logger = logging.getLogger(__name__)


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
        start_time = time.monotonic()
        logger.debug(f"[DB] Executing query: {sql}")
        try:
            async with cls.connection() as cursor:
                await cursor.execute(sql)
                result = await cursor.fetchall()
                elapsed = time.monotonic() - start_time
                row_count = len(result) if result else 0
                logger.info(f"[DB] Query OK in {elapsed:.3f}s, {row_count} rows")
                return result if result else []
        except Exception as e:
            elapsed = time.monotonic() - start_time
            logger.error(f"[DB] Query ERROR after {elapsed:.3f}s: {type(e).__name__}: {e} | SQL: {sql}")
            raise
