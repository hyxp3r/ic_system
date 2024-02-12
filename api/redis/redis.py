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
        self.connection_url = f"redis://{self.REDIS_URL}"

    async def create_connection(self):
        self.connection = aioredis.from_url(
            self.connection_url, db=0)
        return self.connection