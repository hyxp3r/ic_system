from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import delete, func, insert, select

from api.schemas.financeDTO import FinanceSchemaAdd
from api.tasks.cron.finance_update import get_mtime, get_count, get_date_db, get_file_data, make_dates_compare, insert_data, update_insert_data
from api.config import FILE_PATH
from db import sync_session
from db.models.finance import FinancialIndebtedness



class TestFileExist:
    file_path = FILE_PATH
    file_path_error = Path('C://', 'Users', 'e.n.ermakov', 'Desktop', 'file_ic', 'ЭК.xlsx')
  
    def test_file_exist_success(self):
        file_date = get_mtime(file_path = self.file_path)
        print(file_date)
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
    file_path = FILE_PATH

    @staticmethod
    @pytest.fixture
    def delete_from_table_finance():
        with sync_session() as session:
            session.query(FinancialIndebtedness).delete()
            session.commit()
        yield
        with sync_session() as session:
            session.query(FinancialIndebtedness).delete()
            session.commit()

    def test_count_records(self):
        count = get_count()
        assert isinstance(count, int)

    def test_date_db(self, delete_from_table_finance):
        with sync_session() as session:
            stmt_insert = insert(FinancialIndebtedness).values(**self.schema.model_dump())
            session.execute(stmt_insert)
            session.commit()
            file_date = get_date_db()

        assert isinstance(file_date, datetime)

    def test_insert_data(self, delete_from_table_finance):
        data = get_file_data(self.file_path)
        file_date = get_mtime(self.file_path)
        result = insert_data(data, file_date)
        with sync_session() as session:
            stmt = select(func.count(FinancialIndebtedness.id))
            count = session.execute(stmt)
        data_len = len(data)
        assert count.scalar_one() == data_len
        assert result == "Данные успешно добавлены"

    def test_insert_update_data(self, delete_from_table_finance):
        self.test_insert_data(delete_from_table_finance)
        data = get_file_data(self.file_path)
        file_date = datetime.now()
        result = update_insert_data(data, file_date)
        with sync_session() as session:
            stmt = select(func.count(FinancialIndebtedness.id))
            count = session.execute(stmt)
            stmt = select(func.count(FinancialIndebtedness.id)).where(FinancialIndebtedness.status == True)
            count_filter = session.execute(stmt)
        data_len = len(data)
        assert count.scalar_one() == data_len*2
        assert count_filter.scalar_one() == data_len
        assert result == "Данные успешно обновлены и добавлены"


class TestFileCompare:
    file_path = FILE_PATH
    schema = FinanceSchemaAdd(
        fio="Ермаков Евгений Николаевич",
        personal_number="190722",
        contract_number="fadfagf",
        sum=567.35,
        file_created_time=datetime(2023, 11, 5)
        )
    @staticmethod
    @pytest.fixture
    def delete_from_table_finance():
        with sync_session() as session:
            session.query(FinancialIndebtedness).delete()
            session.commit()

    def test_file_compare_true(self, delete_from_table_finance):
        file_date = get_mtime(file_path = self.file_path)
        with sync_session() as session:
            schema = self.schema.__deepcopy__()
            schema.file_created_time = file_date
            stmt_insert = insert(FinancialIndebtedness).values(**schema.model_dump()).returning(FinancialIndebtedness.id)
            id_add = session.execute(stmt_insert).scalar_one()
            session.commit()
            file_date_db = get_date_db()
        result = make_dates_compare(file_date, file_date_db)
        assert result is True

    
    def test_file_compare_false(self, delete_from_table_finance):
        file_date = get_mtime(file_path = self.file_path)
        with sync_session() as session:
            schema = self.schema.__deepcopy__()
            stmt_insert = insert(FinancialIndebtedness).values(**schema.model_dump()).returning(FinancialIndebtedness.id)
            id_add = session.execute(stmt_insert).scalar_one()
            session.commit()
            file_date_db = get_date_db()
        result = make_dates_compare(file_date, file_date_db)
        assert result is False


class TestFileData:
    file_path = FILE_PATH

    def test_get_file_data(self):
        data = get_file_data(self.file_path)
        assert isinstance(data, list)

