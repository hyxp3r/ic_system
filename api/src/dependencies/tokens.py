
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.config import ApiKeySettings
from api.src.dependencies.uow import UOWDep
from api.utils.unitofwork import  UnitOfWork

settings = ApiKeySettings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_current_user(token:str = Depends(oauth2_scheme), uow: UnitOfWork = Depends(UOWDep)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        personal_number: str = payload.get("sub")
        if personal_number is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    #TODO Получение студента по личному номеру
"""
    query = users.select().where(users.c.username == username)
    user = await db.fetch_one(query)
    if user is None:
        raise credentials_exception
    return user

"""