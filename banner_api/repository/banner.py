import sqlalchemy as sa
from db import BannerORM
from dto import BannerContentDTO, BannerDTO, PutBannerDTO
from sqlalchemy.ext.asyncio import AsyncSession


class BannerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_id(self, id_: int) -> BannerDTO | None:
        query = sa.select(BannerORM).where(BannerORM.id == id_)

        scalar = (await self.session.execute(query)).scalar_one_or_none()
        if not scalar:
            return None

        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )

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
        await self.session.refresh(banner)

        return BannerDTO(
            id_=banner.id,
            tag_ids=banner.tag_ids,
            feature_id=banner.feature_id,
            content=BannerContentDTO(text=banner.text, title=banner.title, url=banner.url),
            is_active=banner.is_active,
            created_at=banner.created_at,
            updated_at=banner.updated_at,
        )

    async def delete(self, id_: int) -> None:
        query = sa.delete(BannerORM).where(BannerORM.id == id_)
        await self.session.execute(query)

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

        return BannerDTO(
            id_=scalar.id,
            tag_ids=scalar.tag_ids,
            feature_id=scalar.feature_id,
            content=BannerContentDTO(text=scalar.text, title=scalar.title, url=scalar.url),
            is_active=scalar.is_active,
            created_at=scalar.created_at,
            updated_at=scalar.updated_at,
        )
