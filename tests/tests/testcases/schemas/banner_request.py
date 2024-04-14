from pydantic import BaseModel, Field

from .banner_schema import CreateBannerSchema, UpdateBannerSchema


class GetUserBannerRequest(BaseModel):
    tag_id: int
    feature_id: int
    use_last_revision: bool = False


class GetBannerListRequest(BaseModel):
    tag_id: int | None = None
    feature_id: int | None = None
    limit: int = Field(default=10, gt=1, le=250)
    offset: int = Field(default=0)


class CreateBannerRequest(CreateBannerSchema): ...


class UpdateBannerRequest(UpdateBannerSchema): ...
