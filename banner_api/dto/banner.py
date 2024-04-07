import datetime as dt

from pydantic import BaseModel, Field


class BannerContentDTO(BaseModel):
    title: str
    text: str
    url: str


class BannerDTO(BaseModel):
    id_: str = Field(serialization_alias="banner_id")
    tag_ids: list[int]
    feature_id: int
    content: BannerContentDTO
    is_active: bool
    created_at: dt.datetime
    updated_at: dt.datetime
