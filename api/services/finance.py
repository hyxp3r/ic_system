from typing import Type

from api.schemas.financeDTO import FinanceSchema, FinanceSchemaAdd
from api.utils.unitofwork import IUnitOfWork


class FinanceService:

    async def add_finance(self, uow: IUnitOfWork, finance: FinanceSchemaAdd) -> int | None:
        language_dict = finance.model_dump()
        async with uow:
            language_id = await uow.finances.add_one(language_dict)
            await uow.commit()
        return language_id

    async def get_finance_one(self, uow: IUnitOfWork, id: int):
        async with uow:
            finance = await uow.finances.get_one(id=id)
        return finance
    
    async def get_finance_by_personal_number(self, uow: IUnitOfWork, personal_number: str) -> Type[FinanceSchema]:
        async with uow:
            finance = await uow.finances.get_finance_by_personal_number(personal_number = personal_number)
        return finance

    async def delete_finance_one(self, uow: IUnitOfWork, id: int):
        async with uow:
            finance = await uow.finances.delete_one(id=id)
            await uow.commit()
        return finance

    async def get_count_finance(self, uow: IUnitOfWork) -> int | None:
        async with uow:
            finance = await uow.finances.count_all()
        return finance
