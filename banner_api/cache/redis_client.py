from typing import Any

from redis.asyncio import Redis

from .interface import CacheClientInterface


class RedisCacheClient(CacheClientInterface):
    def __init__(self, redis: Redis, cache_expires_in_seconds: int = 60 * 5) -> None:
        self.redis = redis
        self.cache_expires_in_seconds = cache_expires_in_seconds

    async def get(self, key: Any) -> Any:
        return await self.redis.get(key)

    async def put(self, key: Any, value: Any) -> None:
        await self.redis.set(
            key,
            value,
            self.cache_expires_in_seconds,
        )
