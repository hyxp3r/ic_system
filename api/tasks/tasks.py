from celery import Celery
from pydantic_settings import BaseSettings

from api.tasks.cron.finance_update import update_finance_table
from api.tasks.cron.students_update import update_students_table
from api.tasks.mail.verify_mail import send_verification_code


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


@celery.task(name='update_finance_table')
def update_finance_task():
    update_finance_table()


@celery.task(name='update_students_table')
def update_student_task():
    update_students_table()


@celery.task(name='send_verification_code')
def send_verification_code_task(email: str, code: str):
    send_verification_code(email, code)
