from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_name: str = Field(..., env="DBNAME")

    class Config:
        env_file = "settings/.env"
        env_file_encoding = "utf-8"
