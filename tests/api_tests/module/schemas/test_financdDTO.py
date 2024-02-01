from datetime import datetime

import pytest
from pydantic_core import ValidationError
from contextlib import nullcontext as doesnt_raise

from api.schemas.financeDTO import FinanceSchemaAdd


class TestFinanceSchema:
    
    def test_must_be_int(self):
        data = {
            'fio': 'John Smith',
            'personal_number': '123456',
            'contract_number': 'C123',
            'sum': 1000.0,
            'status': True,
            'file_created_time': datetime.now()
        }
        schema = FinanceSchemaAdd(**data)
        assert schema.personal_number == '123456'

    def test_must_be_int_error(self):
        data = {
            'fio': 'John Smith',
            'personal_number': '123456d',
            'contract_number': 'C123',
            'sum': 1000.0,
            'status': True,
            'file_created_time': datetime.now()
        }
        with pytest.raises(ValidationError):
            schema = FinanceSchemaAdd(**data)
           