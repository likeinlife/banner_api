from repository import BannerRepository
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork:
    session: AsyncSession
    banner: BannerRepository

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.session_maker = session_maker

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self):
        self.session = self.session_maker()

        self.banner = BannerRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
