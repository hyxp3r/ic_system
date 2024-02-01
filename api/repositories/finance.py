from utils.repository import SQLAlchemyRepository

from db import FinancialIndebtedness


class FinanceRepository(SQLAlchemyRepository):
    model = FinancialIndebtedness

