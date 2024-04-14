import datetime as dt

from pydantic import BaseModel, Field


class BaseDTO(BaseModel): ...


class BannerContentDTO(BaseDTO):
    title: str
    text: str
    url: str


class BannerDTO(BaseDTO):
    id_: int = Field(serialization_alias="banner_id")
    tag_ids: set[int]
    feature_id: int
    content: BannerContentDTO
    is_active: bool
    created_at: dt.datetime
    updated_at: dt.datetime


class PutBannerDTO(BaseDTO):
    tag_ids: set[int]
    feature_id: int
    content: BannerContentDTO
    is_active: bool
