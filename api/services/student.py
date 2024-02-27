import random
import string

from fastapi import HTTPException, status
from jose import jwt

from api.config import ApiKeySettings
from api.redis.redis import Redis
from api.schemas.authDTO import Token
from api.tasks.tasks import send_verification_code_task
from api.utils.unitofwork import IUnitOfWork

settings = ApiKeySettings()


SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # не используется, при необходимости можно указать при установке токена


class StudentService:

    async def get_student_by_personal_number(self, uow: IUnitOfWork, personal_number: str):
        async with uow:
            student = await uow.students.get_student_by_personal_number(personal_number=personal_number)
        return student

    async def make_verify_code(self, uow: IUnitOfWork, personal_number: str):
        redis = Redis()
        async with uow:
            student = await uow.students.get_student_by_personal_number(personal_number=personal_number)
        personal_number = student.personal_number
        email = student.email
        if not email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Email is required for sending code'
            )
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        async with redis:
            await redis.set(key=personal_number, value=verification_code, ex=300)
        send_verification_code_task.delay(email, verification_code)
        return email

    async def verify_code(self, uow: IUnitOfWork, personal_number: str, verification_code: str) -> Token:
        redis = Redis()
        async with redis:
            redis_code = await redis.get(personal_number)
        if not redis_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code was't found")
        if redis_code != verification_code:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid verification code')
        token_data = {'sub': personal_number}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        async with uow:
            await uow.students.update_student_api_key(personal_number=personal_number, api_key=token)
            await uow.commit()
        return Token(access_token=token, token_type='bearer')
