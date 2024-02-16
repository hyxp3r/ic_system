from datetime import datetime
from pathlib import Path

import pytest

from api.tasks.cron.finance_update import get_count, get_mtime,  get_file_data, insert_data, finance_update_task
from api.config import FILE_PATH
from db import sync_session
from db.models.finance import FinancialIndebtedness




class TestCron:
    file_path_valid = FILE_PATH
    file_path_invalid = Path('C://', 'e.n.ermakov', 'Desktop', 'file_ic', 'ЭК_ДЗ.xlsx')

    @pytest.fixture
    def insert_test_valid_data(self):
        data = get_file_data(self.file_path_valid)
        file_date = get_mtime(self.file_path_valid)
        insert_data(data, file_date)

    @pytest.fixture
    def insert_test_fake_data(self, mocker):
        data = get_file_data(self.file_path_valid)
        mock_get_mtime = mocker.patch('api.tasks.cron.finance_update.get_mtime')
        mock_get_mtime.return_value = datetime(2024, 10, 11)
        file_date = get_mtime(self.file_path_valid)
        insert_data(data, file_date)

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


    def test_cron_insert(self, delete_from_table_finance):
        result = finance_update_task(self.file_path_valid)
        len_data = len(get_file_data(self.file_path_valid))
        count = get_count()
        assert result == "Данные успешно добавлены"
        assert count == len_data
        
    def test_cron_insert_update(self, delete_from_table_finance, insert_test_fake_data):
        result = finance_update_task(self.file_path_valid)
        len_data = len(get_file_data(self.file_path_valid))
        count = get_count()
        assert result == "Данные успешно обновлены и добавлены"
        assert count == len_data*2
        
    def test_cron_do_nothing(self, delete_from_table_finance, insert_test_valid_data):
        result = finance_update_task(self.file_path_valid)
        len_data = len(get_file_data(self.file_path_valid))
        count = get_count()
        assert count == len_data
        assert result == "Обновление данных не требуется"
    
    def test_cron_file_error(self, delete_from_table_finance, insert_test_valid_data):
        with pytest.raises(FileNotFoundError):
            finance_update_task(self.file_path_invalid)

