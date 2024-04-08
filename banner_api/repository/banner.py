import sqlalchemy as sa
import structlog
from db import BannerORM
from dto import BannerContentDTO, BannerDTO, PutBannerDTO
from sqlalchemy.ext.asyncio import AsyncSession


class BannerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        self._logger = structlog.get_logger()

    async def fetch_id(self, id_: int) -> BannerDTO | None:
        query = sa.select(BannerORM).where(BannerORM.id == id_)

        scalar = (await self.session.execute(query)).scalar_one_or_none()
        if not scalar:
            self._logger.debug("Banner not found", banner_id=id_)
            return None

        self._logger.debug("Banner found", banner_id=id_)
        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )

    async def fetch_tag_feature(self, tag_id: int, feature_id: int) -> BannerDTO | None:
        _logger = self._logger.bind(tag_id=tag_id, feature_id=feature_id)
        query = (
            sa.select(BannerORM).where(BannerORM.feature_id == feature_id).where(BannerORM.tag_ids.contains([tag_id]))
        )

        scalar = (await self.session.execute(query)).scalar_one_or_none()
        if not scalar:
            _logger.debug("Banner not found")
            return None

        _logger.debug("Banner found")
        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )

    async def fetch_list(
        self,
        tag_id: int | None,
        feature_id: int | None,
        offset: int,
        limit: int,
    ) -> list[BannerDTO]:
        _logger = self._logger.bind(tag_id=tag_id, feature_id=feature_id)
        query = sa.select(BannerORM).limit(limit).offset(offset)
        if tag_id is not None:
            query = query.where(BannerORM.tag_ids.contains([tag_id]))
        if feature_id is not None:
            query = query.where(BannerORM.feature_id == feature_id)

        scalar_list = (await self.session.execute(query)).scalars().all()

        _logger.debug("Fetch list")
        return [
            BannerDTO(
                id_=scalar.id,
                tag_ids=scalar.tag_ids,
                feature_id=scalar.feature_id,
                content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
                is_active=scalar.is_active,
                created_at=scalar.created_at,
                updated_at=scalar.updated_at,
            )
            for scalar in scalar_list
        ]

    async def insert(self, dto: PutBannerDTO) -> BannerDTO:
        banner = BannerORM(
            feature_id=dto.feature_id,
            text=dto.content.text,
            title=dto.content.title,
            url=dto.content.url,
            is_active=dto.is_active,
            tag_ids=dto.tag_ids,
        )
        self.session.add(banner)
        await self.session.flush()
        await self.session.refresh(banner)
        self._logger.debug("Banner created", banner_id=banner.id)

        return BannerDTO(
            id_=banner.id,
            tag_ids=banner.tag_ids,
            feature_id=banner.feature_id,
            content=BannerContentDTO(text=banner.text, title=banner.title, url=banner.url),
            is_active=banner.is_active,
            created_at=banner.created_at,
            updated_at=banner.updated_at,
        )

    async def delete(self, id_: int) -> BannerDTO | None:
        query = sa.delete(BannerORM).where(BannerORM.id == id_).returning(BannerORM)
        scalar = (await self.session.execute(query)).scalar_one_or_none()
        if not scalar:
            return None

        self._logger.debug("Banner deleted", banner_id=id_)
        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )

    async def update(self, id_: int, dto: PutBannerDTO) -> BannerDTO | None:
        query = sa.select(BannerORM).where(BannerORM.id == id_)
        scalar = (await self.session.execute(query)).scalar_one_or_none()
        if not scalar:
            return None
        scalar.is_active = dto.is_active
        scalar.text = dto.content.text
        scalar.title = dto.content.title
        scalar.url = dto.content.url
        scalar.tag_ids = dto.tag_ids
        await self.session.flush()
        self._logger.debug("Banner updated", banner_id=id_)

        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )
