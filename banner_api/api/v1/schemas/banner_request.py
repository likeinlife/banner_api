from pydantic import BaseModel, Field

from .banner_schema import CreateBannerSchema, UpdateBannerSchema


class GetUserBannerRequest(BaseModel):
    tag_id: int
    feature_id: int
    use_last_revision: bool = False


class GetBannerListRequest(BaseModel):
    tag_id: int | None = None
    feature_id: int | None = None


class CreateBannerRequest(CreateBannerSchema):
    ...


class UpdateBannerRequest(UpdateBannerSchema):
    ...


class DeleteBannerRequest(BaseModel):
    id_: int = Field(serialization_alias="id")
