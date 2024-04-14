from cache import CacheService
from dto import BannerContentDTO, BannerDTO
from fastapi import HTTPException, status
from uow import UnitOfWork

from .interface import IBannerUseCases


# ruff: noqa: ARG002
class UserBannerUserCases(IBannerUseCases):
    def __init__(self, uow: UnitOfWork, cache_service: CacheService[BannerDTO]) -> None:
        self.uow = uow
        self.cache_service = cache_service

    async def user_banner(
        self,
        tag_id: int,
        feature_id: int,
        use_last_revision: bool,
    ) -> BannerContentDTO:
        result = None
        if not use_last_revision:
            result = await self.cache_service.fetch([tag_id, feature_id])
        if not result:
            async with self.uow:
                result = await self.uow.banner.fetch_tag_feature(tag_id, feature_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Баннер не найден")
        await self.cache_service.put([tag_id, feature_id], result)
        if result.is_active:
            return result.content
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Баннер не найден")

    async def banner_list(
        self,
        tag_id: int | None,
        feature_id: int | None,
        offset: int,
        limit: int,
    ) -> list[BannerDTO]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")

    async def create(
        self,
        tag_ids: set[int],
        feature_id: int,
        title: str,
        text: str,
        url: str,
        is_active: bool,
    ) -> BannerDTO:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")

    async def update(
        self,
        id_: int,
        tag_ids: set[int],
        feature_id: int,
        title: str,
        text: str,
        url: str,
        is_active: bool,
    ) -> BannerDTO:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")

    async def delete(
        self,
        id_: int,
    ) -> BannerDTO:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")

    async def delete_by_query(
        self,
        feature_id: int | None = None,
        tag_id: int | None = None,
    ) -> None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет доступа")
