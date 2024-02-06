from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import delete, insert

from api.schemas.financeDTO import FinanceSchemaAdd
from api.tasks.cron.finance_update import get_mtime, get_count, get_date_db
from api.config import FILE_PATH
from db import sync_session
from db.models.finance import FinancialIndebtedness

class TestFileExist:
    file_path = FILE_PATH
    file_path_error = Path('C://', 'Users', 'e.n.ermakov', 'Desktop', 'file_ic', 'ЭК.xlsx')
  
    def test_file_exist_success(self):
        file_date = get_mtime(file_path = self.file_path)
        assert isinstance(file_date, datetime)

    
    def test_file_exist_error(self):
        with pytest.raises(FileNotFoundError):
            data = get_mtime(file_path= self.file_path_error)


class TestDB:

    schema = FinanceSchemaAdd(
        fio="Ермаков Евгений Николаевич",
        personal_number="190722",
        contract_number="fadfagf",
        sum=567.35,
        file_created_time=datetime.now()
        )

    def test_count_records(self):
        count = get_count()
        assert isinstance(count, int)

    def test_date_db(self):
        with sync_session() as session:
            stmt_insert = insert(FinancialIndebtedness).values(**self.schema.model_dump()).returning(FinancialIndebtedness.id)
            id_add = session.execute(stmt_insert).scalar_one()
            session.commit()
            file_date = get_date_db()

            stmt_delete = delete(FinancialIndebtedness).filter_by(id = id_add).returning(FinancialIndebtedness.id)
            id_delete = session.execute(stmt_delete)
            session.commit()

        assert isinstance(file_date, datetime)