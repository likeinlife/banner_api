import abc

from dto import BannerContentDTO, BannerDTO


class IBannerUseCases(abc.ABC):
    @abc.abstractmethod
    async def user_banner(
        self,
        tag_id: int,
        feature_id: int,
        use_last_revision: bool,
    ) -> BannerContentDTO:
        ...

    @abc.abstractmethod
    async def banner_list(
        self,
        tag_id: int | None,
        feature_id: int | None,
        offset: int,
        limit: int,
    ) -> list[BannerDTO]:
        ...

    @abc.abstractmethod
    async def create(
        self,
        tag_ids: set[int],
        feature_id: int,
        title: str,
        text: str,
        url: str,
        is_active: bool,
    ) -> BannerDTO:
        ...

    @abc.abstractmethod
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
        ...

    @abc.abstractmethod
    async def delete(
        self,
        id_: int,
    ) -> BannerDTO:
        ...
