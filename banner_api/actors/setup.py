import asyncio
import typing as tp
from functools import lru_cache

import dramatiq
import structlog
from core import settings
from db.connection import create_engine, create_session_maker
from uow import UnitOfWork

from . import configure_dramatiq

logger = structlog.get_logger()
configure_dramatiq(host=settings.cache.host, port=settings.cache.port)


@lru_cache(maxsize=1)
def _get_uow() -> UnitOfWork:
    _engine = create_engine(settings.db.async_url)
    _session_maker = create_session_maker(_engine)
    return UnitOfWork(_session_maker)


async def delete_query(
    feature_id: int | None = None,
    tag_id: int | None = None,
) -> tp.Sequence[int]:
    uow = _get_uow()
    async with uow:
        result = await uow.banner.delete_by_query(feature_id=feature_id, tag_id=tag_id)
        await uow.commit()
        return result


@dramatiq.actor
def banner_query_delete_worker(
    feature_id: int | None = None,
    tag_id: int | None = None,
):
    result = asyncio.run(delete_query(feature_id=feature_id, tag_id=tag_id))
    logger.info("Deleting query", feature_id=feature_id, tag_id=tag_id, result=result)
