import hashlib
import time
import logging
from typing import Any, Optional
from collections import OrderedDict

logger = logging.getLogger(__name__)


class CacheEntry:
    __slots__ = ("value", "expires_at", "created_at", "hit_count")

    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = time.time() + ttl
        self.created_at = time.time()
        self.hit_count = 0

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def touch(self) -> None:
        self.hit_count += 1


class TimedCache:
    def __init__(self, max_size: int = 500, default_ttl: int = 300):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    def _make_key(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[:32]

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry is None:
            self._misses += 1
            return None
        if entry.is_expired():
            del self._cache[key]
            self._misses += 1
            return None
        entry.touch()
        self._hits += 1
        self._cache.move_to_end(key)
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
        actual_ttl = ttl if ttl is not None else self._default_ttl
        self._cache[key] = CacheEntry(value, actual_ttl)

    def delete(self, key: str) -> bool:
        return self._cache.pop(key, None) is not None

    def clear(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def stats(self) -> dict[str, Any]:
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 2),
            "size": len(self._cache),
            "max_size": self._max_size,
        }


class QueryCache:
    _instance: Optional["QueryCache"] = None

    def __init__(self):
        self._sql_cache = TimedCache(max_size=200, default_ttl=60)
        self._agent_cache = TimedCache(max_size=100, default_ttl=300)
        self._enabled = True

    @classmethod
    def get_instance(cls) -> "QueryCache":
        if cls._instance is None:
            cls._instance = QueryCache()
        return cls._instance

    def _normalize_sql(self, sql: str) -> str:
        return " ".join(sql.lower().split())

    def get_sql_result(self, sql: str) -> Optional[dict[str, Any]]:
        if not self._enabled:
            return None
        key = self._normalize_sql(sql)
        return self._sql_cache.get(key)

    def set_sql_result(self, sql: str, result: dict[str, Any], ttl: int = 60) -> None:
        if not self._enabled:
            return
        key = self._normalize_sql(sql)
        self._sql_cache.set(key, result, ttl)
        logger.info(f"[CACHE] SQL result cached: {key[:8]}...")

    def get_agent_response(self, query: str) -> Optional[str]:
        if not self._enabled:
            return None
        key = hashlib.sha256(query.encode()).hexdigest()[:32]
        return self._agent_cache.get(key)

    def set_agent_response(self, query: str, response: str, ttl: int = 300) -> None:
        if not self._enabled:
            return
        key = hashlib.sha256(query.encode()).hexdigest()[:32]
        self._agent_cache.set(key, response, ttl)
        logger.info(f"[CACHE] Agent response cached")

    def invalidate(self) -> None:
        self._sql_cache.clear()
        self._agent_cache.clear()

    def stats(self) -> dict[str, Any]:
        return {
            "sql": self._sql_cache.stats(),
            "agent": self._agent_cache.stats(),
            "enabled": self._enabled,
        }


query_cache = QueryCache.get_instance()