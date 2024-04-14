import actors
import cache
from core import configure_logging, settings
from db import create_engine, create_session_maker
from dependency_injector import providers as pr
from dependency_injector.containers import DeclarativeContainer
from dto import BannerDTO
from uow import UnitOfWork


class Container(DeclarativeContainer):
    logger: pr.Resource = pr.Resource(
        configure_logging,
        level=settings.logging.level,
        json_format=settings.logging.json_format,
    )

    dramatiq_configuration: pr.Resource = pr.Resource(
        actors.configure_dramatiq,
        settings.cache.host,
        settings.cache.port,
    )

    engine: pr.Singleton = pr.Singleton(create_engine, settings.db.async_url)
    session_maker: pr.Singleton = pr.Singleton(create_session_maker, engine)

    uow: pr.Singleton = pr.Singleton(UnitOfWork, session_maker)
    redis_connection: pr.Singleton = pr.Singleton(
        cache.create_redis_connection,
        settings.cache.host,
        settings.cache.port,
    )
    redis_client: pr.Singleton = pr.Singleton(
        cache.RedisCacheClient,
        redis_connection,
        settings.cache.expire_time_in_seconds,
    )
    banner_cache_client: pr.Singleton = pr.Singleton(
        cache.CacheService,
        redis_client,
        BannerDTO,
    )
