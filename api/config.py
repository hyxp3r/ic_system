from pathlib import Path

from pydantic_settings import BaseSettings

FILE_PATH = Path('/app', 'data', 'ЭК_ДЗ.CSV')


class ApiKeySettings(BaseSettings):
    secret_key: str
    algorithm: str

    class Config:
        env_prefix = 'AUTH_'
        env_file = '.env'


class RedisSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'


class MailSettings(BaseSettings):
    from_email: str
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

    class Config:
        env_prefix = 'MAIL_'
        env_file = '.env'


class TandemSettings(BaseSettings):
    server: str
    database: str
    uid: str
    pwd: str

    class Config:
        env_prefix = 'TANDEM_'
        env_file = '.env'
