from datetime import datetime
import os

from httpx import AsyncClient
import pytest

from api.schemas.financeDTO import FinanceSchemaAdd
from api.services.finance import FinanceService
from api.utils.unitofwork import UnitOfWork
from db import FinancialIndebtedness, sync_session
from tests.api_tests.module.api.routers.test_students_router import add_student_with_email



@pytest.fixture
async def add_delete_table_finance():
    schema = FinanceSchemaAdd(
        fio="Ермаков Евгений Николаевич",
        personal_number="190722",
        contract_number="fadfagf",
        sum=567.35,
        file_created_time=datetime(2024, 11, 5)
        )
    id_add = await FinanceService().add_finance(UnitOfWork(), schema)
    yield
    with sync_session() as session:
        session.query(FinancialIndebtedness).delete()
        session.commit()

class TestFinanceRouter:

    async def test_finance_get_200(self, ac: AsyncClient,add_student_with_email,  add_delete_table_finance, ):
        headers = {
            "Authorization": f"Bearer {os.environ.get('TOKEN')}",
            }
        response = await ac.get("finances",
                                headers= headers
                                )
        assert response.status_code == 200

    async def test_finance_get_401(self, ac: AsyncClient,add_student_with_email,  add_delete_table_finance, ):
        headers = {
            "Authorization": "Bearer sgsg",
            }
        response = await ac.get("finances",
                                headers= headers
                                )
        assert response.status_code == 401

    async def test_finance_get_422(self, ac: AsyncClient,add_student_with_email,  add_delete_table_finance, ):
        headers = {
            "token": "Bearer sgsg",
            }
        response = await ac.get("finances",
                                headers= headers
                                )
        assert response.status_code == 422