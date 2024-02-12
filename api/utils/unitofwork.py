from abc import ABC, abstractmethod
from typing import Type

from api.repositories.finance import FinanceRepository
from api.repositories.students import StudentRepository
from db import async_session_maker


class IUnitOfWork(ABC):
    finances: Type[FinanceRepository]
    students: Type[StudentRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.finances = FinanceRepository(self.session)
        self.students = StudentRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
