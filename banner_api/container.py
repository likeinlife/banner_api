from core import configure_logging, settings
from db import create_engine, create_session_maker
from dependency_injector import providers as pr
from dependency_injector.containers import DeclarativeContainer
from uow import UnitOfWork


class Container(DeclarativeContainer):
    logger: pr.Resource = pr.Resource(
        configure_logging,
        level=settings.logging.level,
        json_format=settings.logging.json_format,
    )

    engine: pr.Singleton = pr.Singleton(create_engine, settings.db.async_url)
    session_maker: pr.Singleton = pr.Singleton(create_session_maker, engine)

    uow: pr.Singleton = pr.Singleton(UnitOfWork, session_maker)
