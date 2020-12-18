from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_api_token: str = Field(..., env="TG_API_TOKEN")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    static_folder: Path = Field(..., env="STATIC_FOLDER")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
