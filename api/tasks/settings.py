from celery import Celery
from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    broker_url: str
    result_backend: str
    class Config:
        env_prefix = 'CELERY_'
        env_file = '.env'


settings = CelerySettings()
celery = Celery(__name__)
celery.conf.broker_url = settings.broker_url
celery.conf.result_backend = settings.result_backend


celery.conf.beat_schedule = {
    "create_task": {
        "task": "create_file",
        "schedule": 89.0,
    },
}
celery.conf.timezone = "UTC"