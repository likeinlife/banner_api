from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    domain: str = Field("http://127.0.0.1:8000", init=False)
    api_url: str = Field("/api/v1", init=False)


settings = Settings()
