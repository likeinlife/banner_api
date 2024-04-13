from api.dependencies import Role
from cache import CacheService
from container import Container
from dependency_injector.wiring import Provide, inject
from dto import BannerDTO
from typing_extensions import assert_never
from uow import UnitOfWork

from .banner import AdminBannerUseCases, IBannerUseCases, UserBannerUserCases


@inject
def banner_usecase_factory(
    role: Role,
    uow: UnitOfWork = Provide[Container.uow],
    cache_service: CacheService[BannerDTO] = Provide[Container.banner_cache_client],
) -> IBannerUseCases:
    match role:
        case Role.ADMIN:
            return AdminBannerUseCases(uow, cache_service)
        case Role.USER:
            return UserBannerUserCases(uow, cache_service)
        case _:
            assert_never(role)
