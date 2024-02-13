
from fastapi import  HTTPException
from fastapi import Header
from jose import JWTError, jwt

from api.config import ApiKeySettings
from api.src.dependencies.uow import UOWDep
from api.services.student import StudentService

settings = ApiKeySettings()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_current_user(uow: UOWDep, token: str = Header(convert_underscores=False)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        personal_number: str = payload.get("sub")
        if personal_number is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await StudentService().get_student_by_personal_number(uow, personal_number)
    return user

