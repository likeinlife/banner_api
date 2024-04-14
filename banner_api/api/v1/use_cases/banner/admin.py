from actors.setup import banner_query_delete_worker
from cache import CacheService
from dto import BannerContentDTO, BannerDTO
from dto.banner import PutBannerDTO
from fastapi import HTTPException, status
from uow import UnitOfWork

from .interface import IBannerUseCases


class AdminBannerUseCases(IBannerUseCases):
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
        return result.content

    async def banner_list(
        self,
        tag_id: int | None,
        feature_id: int | None,
        offset: int,
        limit: int,
    ) -> list[BannerDTO]:
        async with self.uow:
            return await self.uow.banner.fetch_list(
                tag_id,
                feature_id,
                offset,
                limit,
            )

    async def create(
        self,
        tag_ids: set[int],
        feature_id: int,
        title: str,
        text: str,
        url: str,
        is_active: bool,
    ) -> BannerDTO:
        async with self.uow:
            result = await self.uow.banner.insert(
                PutBannerDTO(
                    tag_ids=tag_ids,
                    feature_id=feature_id,
                    is_active=is_active,
                    content=BannerContentDTO(title=title, text=text, url=url),
                )
            )
            await self.uow.commit()
            return result

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
        async with self.uow:
            dto = await self.uow.banner.update(
                id_,
                PutBannerDTO(
                    tag_ids=tag_ids,
                    feature_id=feature_id,
                    is_active=is_active,
                    content=BannerContentDTO(title=title, text=text, url=url),
                ),
            )
            if not dto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Баннер не найден")
            await self.uow.commit()
            return dto

    async def delete(
        self,
        id_: int,
    ) -> BannerDTO:
        async with self.uow:
            dto = await self.uow.banner.delete(id_)
            if not dto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Баннер не найден")
            await self.uow.commit()
            return dto

    async def delete_by_query(
        self,
        feature_id: int | None = None,
        tag_id: int | None = None,
    ) -> None:
        if feature_id is None and tag_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо передать хотя бы один параметр",
            )
        banner_query_delete_worker.send(feature_id=feature_id, tag_id=tag_id)
