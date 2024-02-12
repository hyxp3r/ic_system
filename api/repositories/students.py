from typing import Type
from fastapi import HTTPException, status
from sqlalchemy import select, update

from api.utils.repository import SQLAlchemyRepository
from db import Students
from api.schemas.studentDTO import StudentSchema


class StudentRepository(SQLAlchemyRepository):
    
    model = Students

    async def get_student_by_personal_number(self, personal_number:str) -> Type[StudentSchema]:
        stmt = select(self.model).filter_by(personal_number = personal_number)
        res = await self.session.execute(stmt)
        res = res.one_or_none()
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Record not found')
        student = res[0].to_read_model()
        return student
    

    async def update_student_api_key(self, personal_number:str, api_key:str) -> Type[StudentSchema]:
        stmt = update(self.model).filter_by(personal_number = personal_number).values(api_key = api_key)
        res = await self.session.execute(stmt)
        

