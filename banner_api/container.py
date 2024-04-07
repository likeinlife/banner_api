from dependency_injector import providers as pr
from dependency_injector.containers import DeclarativeContainer

from .core import configure_logging, settings


class Container(DeclarativeContainer):
    logger = pr.Resource(
        configure_logging,
        level=settings.logging.level,
        json_format=settings.logging.json_format,
    )
