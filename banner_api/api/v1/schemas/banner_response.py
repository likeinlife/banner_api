from pydantic import BaseModel, Field


class CreateBannerResponse(BaseModel):
    id_: int = Field(serialization_alias="id")
