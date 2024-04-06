from pydantic_settings import BaseSettings


class AdminSettings(BaseSettings):
    login: str
    password: str
    key: str

    class Config:
        env_prefix = 'LOGIN_'
        env_file = '.env'
