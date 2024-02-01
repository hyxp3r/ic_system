from typing import Any, Dict

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class BaseDBModel(BaseModel):
    url_sync: str
    url_async: str
    engine_config: Dict[str, Any] = {}
    echo: int = 0

    @property
    def engine(self) -> Engine:
        return create_engine(str(self.url_sync), **self.engine_config, echo=self.echo)

    @property
    def async_engine(self) -> AsyncEngine:
        return create_async_engine(str(self.url_async), **self.engine_config, echo=self.echo)


class DBSettings(BaseDBModel, BaseSettings):
    class Config:
        env_prefix = 'DB_'
        env_file = '.env'

    def setup_engine_sync(self) -> Engine:
        engine = self.engine
        return engine

    def setup_engine_async(self) -> AsyncEngine:
        engine = self.async_engine
        return engine
