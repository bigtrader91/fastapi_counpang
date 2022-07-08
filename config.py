from click import password_option
from psycopg2 import DatabaseError
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    host: str = "localhost"
    database: str = "coupang"
    id: str = "postgres"
    password: str = "postgres"
    port: int = 5432
    db_uri: str = "postgresql://postgres:postgres@localhost/coupang"
    best_uri: str = "postgresql://best:1234@localhost/coupang"
    search_uri: str = "postgresql://search:1234@localhost/coupang"
    telgm_token: str = "1108135935:AAEzD9fUZxII258ELQm3ah_gej1E3LqLlmU"
    chat_id: int = 1069639277
    ACCESS_KEY: str = "c2d7d0f8-687a-43b6-9ebe-cc2f413c9a56"
    SECRET_KEY: str = "a98b7ae97ad5e63bbef6adb1e5667b9f779d72e9"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
