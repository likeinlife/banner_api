from api.dependencies import Role
from cache import CacheService
from container import Container
from dependency_injector.wiring import Provide, inject
from dto import BannerDTO
from uow import UnitOfWork

from .banner import BannerUseCases


@inject
def banner_usecase_factory(
    role: Role,  # noqa
    uow: UnitOfWork = Provide[Container.uow],
    cache_service: CacheService[BannerDTO] = Provide[Container.banner_cache_client],
) -> BannerUseCases:
    return BannerUseCases(uow, cache_service)
