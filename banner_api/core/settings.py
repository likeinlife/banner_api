from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

    host: str = Field(init=False)
    port: int = Field(init=False)
    user: str = Field(init=False)
    password: str = Field(init=False)
    database: str = Field(init=False)

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")

    host: str = Field(init=False)
    port: int = Field(init=False)
    expire_time_in_seconds: int = Field(default=60 * 5, init=False)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    title: str = Field(init=False)
    version: str = Field(init=False)
    debug: bool = Field(init=False)


class LoggingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOGGING_", extra="ignore")

    level: str = Field(default="INFO", init=False)
    json_format: bool = Field(default=False, init=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    logging: LoggingConfig = LoggingConfig()
    db: DBSettings = DBSettings()
    cache: CacheSettings = CacheSettings()


settings = Settings()
