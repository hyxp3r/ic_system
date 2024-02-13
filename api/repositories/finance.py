from typing import Type

from fastapi import HTTPException, status
from sqlalchemy import select

from api.schemas.financeDTO import FinanceSchema
from api.utils.repository import SQLAlchemyRepository
from db import FinancialIndebtedness


class FinanceRepository(SQLAlchemyRepository):

    model = FinancialIndebtedness

    async def get_finance_by_personal_number(self, personal_number: str) -> Type[FinanceSchema]:
        stmt = select(self.model).filter_by(personal_number=personal_number, status=True)
        res = await self.session.execute(stmt)
        res = res.one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')
        return res[0].to_read_model()
