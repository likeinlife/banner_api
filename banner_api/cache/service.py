import hashlib
import typing as tp

import backoff
from constants import BACKOFF_MAX_TIME
from dto import BaseDTO
from pydantic import TypeAdapter

from .interface import CacheClientInterface

M = tp.TypeVar("M", bound=BaseDTO)


class CacheService(tp.Generic[M]):
    def __init__(self, cache_client: CacheClientInterface, model: type[M]) -> None:
        self.cache_client = cache_client
        self.model = model

    @backoff.on_exception(backoff.expo, Exception, max_time=BACKOFF_MAX_TIME)
    async def fetch(self, query: tp.Collection) -> M | None:
        key = self._generate_key(*query)
        data = await self.cache_client.get(key)
        if not data:
            return None
        return TypeAdapter(self.model).validate_json(data)

    @backoff.on_exception(backoff.expo, Exception, max_time=BACKOFF_MAX_TIME)
    async def put(self, query: tp.Collection, value: M) -> None:
        key = self._generate_key(*query)
        await self.cache_client.put(key, value.model_dump_json())

    @staticmethod
    def _generate_key(*args: tp.Any) -> str:
        return hashlib.sha256(str(args).encode("utf-8")).hexdigest()
