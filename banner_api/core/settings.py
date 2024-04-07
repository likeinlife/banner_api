from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    title: str = Field(init=False)
    version: str = Field(init=False)

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")


class LoggingConfig(BaseSettings):
    level: str = Field(default="INFO", init=False)
    json_format: bool = Field(default=False, init=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
