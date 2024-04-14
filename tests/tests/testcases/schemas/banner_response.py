from pydantic import BaseModel, Field


class CreateBannerResponse(BaseModel):
    id_: int = Field(validation_alias="id")
