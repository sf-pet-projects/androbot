from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_api_token: str = Field(..., env="TG_API_TOKEN")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    static_folder: Path = Field("templates", env="STATIC_FOLDER")
    fsm_redis_host: str = Field("", env="REDIS_HOST")
    fsm_redis_port: int = Field(6379, env="REDIS_PORT")
    fsm_redis_db: int = Field(5, env="REDIS_DB")
    fsm_redis_password: str = Field("", env="REDIS_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
