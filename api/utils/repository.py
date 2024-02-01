from abc import ABC, abstractmethod
from typing import Any, Union

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import BaseTable


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, data: dict[str, Any]) -> Union[int, Any]:
        raise NotImplementedError()

    @abstractmethod
    async def get_one(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_records(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_records(self) -> None:
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):

    model: BaseTable = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict[str, Any]) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_many(self, **filter_by) -> None:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def get_one(self, id: int) -> BaseModel | None:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        res = res.one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')
        return res[0].to_read_model()

    async def update_records(self, id: int, **update_data: dict) -> int:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')
        stmt = update(self.model).filter_by(id=id).values(**update_data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_records(self, id: int) -> int:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')
        stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def count_all(self) -> int:
        stmt = select(func.count(self.model.id))
        count = await self.session.execute(stmt)
        return count.scalar_one()
