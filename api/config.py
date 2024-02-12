from pathlib import Path

from pydantic_settings import BaseSettings

FILE_PATH = Path('C://', 'Users', 'e.n.ermakov', 'Desktop', 'file_ic', 'ЭК_ДЗ.xlsx')

class ApiKeySettings(BaseSettings):
    secret_key: str

    class Config:
        env_prefix = 'AUTH_'
        env_file = '.env'


class RedisSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'