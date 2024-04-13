from api.dependencies import Role
from cache import CacheService
from dto import BannerContentDTO, BannerDTO
from dto.banner import PutBannerDTO
from fastapi import HTTPException, status
from uow import UnitOfWork


class BannerUseCases:
    def __init__(self, uow: UnitOfWork, cache_service: CacheService[BannerDTO]) -> None:
        self.uow = uow
        self.cache_service = cache_service

    async def user_banner(
        self,
        role: Role,
        tag_id: int,
        feature_id: int,
        use_last_revision: bool,
    ) -> BannerContentDTO:
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
        if role == Role.ADMIN:
            return result.content
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Баннер не найден")

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
