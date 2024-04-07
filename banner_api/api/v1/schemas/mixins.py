from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(default=10)
    offset: int = Field(default=0)
