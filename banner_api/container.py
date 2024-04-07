from core import configure_logging, settings
from dependency_injector import providers as pr
from dependency_injector.containers import DeclarativeContainer


class Container(DeclarativeContainer):
    logger: pr.Resource = pr.Resource(
        configure_logging,
        level=settings.logging.level,
        json_format=settings.logging.json_format,
    )
