from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    tg_api_token: str = Field(..., env="TG_API_TOKEN")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_name: str = Field(..., env="DB_NAME")
    answers_types: str = Field(..., env="ANSWERS_TYPES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
