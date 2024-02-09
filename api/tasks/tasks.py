from celery import Celery
from pydantic_settings import BaseSettings

from api.tasks.cron.finance_update import finance_update_task


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
    'create_task': {
        'task': 'update_finance_table',
        'schedule': 89.0,
    },
}
celery.conf.timezone = 'UTC'


@celery.task(name = "update_finance_table")
def update_finance_table():
     finance_update_task()