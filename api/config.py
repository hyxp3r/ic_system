from pathlib import Path

from pydantic_settings import BaseSettings

FILE_PATH = Path('C://', 'Users', 'e.n.ermakov', 'Desktop', 'file_ic', 'ЭК_ДЗ.xlsx')


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
    uid:str
    pwd: str

    class Config:
        env_prefix = 'TANDEM_'
        env_file = '.env'


connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.0.150.141;DATABASE=Tandem_prod;UID=pao;PWD=passpao"