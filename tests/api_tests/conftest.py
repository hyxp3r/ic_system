import asyncio

import pytest

from db.base import  metadata, sync_engine
from db.models.finance import FinancialIndebtedness


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    metadata.create_all(bind=sync_engine)
    yield
    metadata.drop_all(bind=sync_engine)
    

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()