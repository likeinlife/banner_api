from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(default=10, gt=1, le=250)
    offset: int = Field(default=0)
