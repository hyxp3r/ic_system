from datetime import datetime

import pytest
from fastapi import HTTPException

from api.services.finance import FinanceService
from api.schemas.financeDTO import FinanceSchemaAdd, FinanceSchema
from api.utils.unitofwork import UnitOfWork

class TestFinanceService:
    schema = FinanceSchemaAdd(
        fio="Ермаков Евгений Николаевич",
        personal_number="190722",
        contract_number="fadfagf",
        sum=567.35,
        file_created_time=datetime(2024, 11, 5)
        )
    
    async def test_fincance_add(self):
        id_add = await FinanceService().add_finance(UnitOfWork(), self.schema)
        assert isinstance(id_add, int)
        id_delete = await FinanceService().delete_finance_one(UnitOfWork(), id_add)
        assert isinstance(id_delete, int)

    async def test_finance_delete(self):
        id_add = await FinanceService().add_finance(UnitOfWork(), self.schema)
        assert isinstance(id_add, int)
        id_delete = await FinanceService().delete_finance_one(UnitOfWork(), id_add)
        assert isinstance(id_delete, int)
        assert id_add == id_delete

    async def test_fincance_get(self):
        id = await FinanceService().add_finance(UnitOfWork(), self.schema)
        finance = await FinanceService().get_finance_one(UnitOfWork(), id = id)
        assert isinstance(finance, FinanceSchema)
        id_delete = await FinanceService().delete_finance_one(UnitOfWork(), id)
        assert isinstance(id_delete, int)

    async def test_fincance_get_error(self): 
        with pytest.raises(HTTPException):
         finance = await FinanceService().get_finance_one(UnitOfWork(), id = 500)

    async def test_fincance_get_count(self): 
       count = await FinanceService().get_count_finance(UnitOfWork())
       assert isinstance(count, int)
        
    