import sqlalchemy as sa

from api.schemas.financeDTO import FinanceSchema
from db.base import BaseTable


class FinancialIndebtedness(BaseTable):
    """Таблица c задолженностями студентов"""

    fio = sa.Column(sa.String(255), nullable=False, doc='ФИО студента')
    personal_number = sa.Column(sa.String(10), nullable=False, doc='Личный номер студента')
    contract_number = sa.Column(sa.String(255), nullable=False, doc='Номер договора')
    sum = sa.Column(sa.Float(decimal_return_scale=2), nullable=False, doc='Номер договора')
    status = sa.Column(sa.Boolean, nullable=False, default=True, server_default='1', doc='Актуальность')
    file_created_time = sa.Column(sa.TIMESTAMP, nullable=False, doc='Дата загрузки файла')

    def to_read_model(self) -> FinanceSchema:
        return FinanceSchema(
            id=self.id,
            fio=self.fio,
            personal_number=self.personal_number,
            contract_number=self.contract_number,
            sum=self.sum,
            status=self.status,
            file_created_time=self.file_created_time,
            created_at=self.created_at
        )
    
    def file_date(self):
        return self.file_created_time



