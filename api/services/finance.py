from api.schemas.financeDTO import FinanceSchemaAdd
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

    async def get_count_finance(self, uow: IUnitOfWork) -> int | None:
        async with uow:
            finance = await uow.finances.count_all()
        return finance
