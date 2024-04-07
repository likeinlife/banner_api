from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


def create_engine(url: str) -> AsyncEngine:
    return create_async_engine(url)


def create_session_maker(engine: AsyncEngine):
    return async_sessionmaker(bind=engine)
