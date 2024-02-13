import os

from redis import asyncio as aioredis

from api.config import RedisSettings

settings = RedisSettings()


class Redis:
    """
    config для подключения Redis
    """

    def __init__(self):
        self.REDIS_URL = settings.url
        self.connection_url = f'redis://{self.REDIS_URL}'

    async def __aenter__(self):
        self.connection = aioredis.from_url(self.connection_url, db=0)

    async def __aexit__(self, *args):
        await self.connection.close()

    async def get(self, key: str) -> str:
        result = await self.connection.get(key)
        if result:
            return result.decode()

    async def set(self, key: str, value: str, ex: int = None):
        result = await self.connection.set(name=key, value=value, ex=ex)
        return result
