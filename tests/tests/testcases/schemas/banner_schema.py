import datetime as dt

from pydantic import BaseModel, Field


class BannerContentSchema(BaseModel):
    title: str
    text: str
    url: str


class BannerSchema(BaseModel):
    id_: int = Field(serialization_alias="banner_id", validation_alias="banner_id")
    tag_ids: list[int]
    feature_id: int
    content: BannerContentSchema
    is_active: bool
    created_at: dt.datetime
    updated_at: dt.datetime


class CreateBannerSchema(BaseModel):
    tag_ids: set[int]
    feature_id: int
    content: BannerContentSchema
    is_active: bool


class UpdateBannerSchema(BaseModel):
    tag_ids: set[int]
    feature_id: int
    content: BannerContentSchema
    is_active: bool
