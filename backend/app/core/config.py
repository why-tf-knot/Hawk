from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hawk API"
    api_prefix: str = ""
    mock_mode: bool = True
    earth_engine_project: str = ""
    geocoding_provider: str = "demo"
    redis_url: str | None = None
    database_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
