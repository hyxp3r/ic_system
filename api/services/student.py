import random
import string

from fastapi import HTTPException, status
from jose import JWTError, jwt

from api.utils.unitofwork import IUnitOfWork
from api.redis.redis import Redis
from api.config import ApiKeySettings

settings = ApiKeySettings()


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class StudentService:

    async def get_student_by_personal_number(self, uow: IUnitOfWork, personal_number: str):
        async with uow:
            student = await uow.students.get_student_by_personal_number(personal_number=personal_number)
        return student
    

    async def make_verify_code(self, uow: IUnitOfWork, personal_number: str):
        async with uow:
            student = await uow.students.get_student_by_personal_number(personal_number=personal_number)
        personal_number = student.personal_number
        email = student.email
        print(email)

        verification_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        redis = Redis()
        redis_conn = await redis.create_connection()
        await redis_conn.set(name=personal_number, value=verification_code, ex=300)
        await redis_conn.close()
        return verification_code
    
    async def verify_code(self, uow: IUnitOfWork, personal_number:str, verification_code:str):
        
        redis = Redis()
        redis_conn = await redis.create_connection()
        redis_code = await redis_conn.get(personal_number)
        await redis_conn.close()
        if redis_code:
            redis_code = redis_code.decode()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code was't found")

        if redis_code == verification_code:
            token_data = {"sub": personal_number}
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            async with uow:
                await uow.students.update_student_api_key(personal_number=personal_number, api_key=token)
                await uow.commit()

            return {"access_token": token, "token_type": "bearer"}  
        
