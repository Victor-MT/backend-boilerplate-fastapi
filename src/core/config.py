from pydantic import BaseSettings
from core.utils import get_env_file_path
import os

class Settings(BaseSettings):
    DATABASE_PORT: int = os.getenv("DATABASE_PORT")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_HOSTNAME: str = os.getenv("POSTGRES_HOSTNAME")
    DB_CONTAINER: str = os.getenv("DB_CONTAINER")
    HOME_PATH: str = os.getenv("HOME")

    class Config:
        env_file = get_env_file_path()

class SettingsSingleton:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Settings()
        return cls.__instance


settings = SettingsSingleton().get_instance()