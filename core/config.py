from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database URL — обязательно
    database_url: str = Field(..., env="DATABASE_URL")

    # Telegram bot token
    bot_token: str = Field(..., env="BOT_TOKEN")

    # Optional
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"


settings = Settings()
