from fastapi import APIRouter, status

from api.src.dependencies.uow import UOWDep
from api.services.student import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

@router.get("/creating_codes",
            status_code=status.HTTP_200_OK,)
async def make_code(uow: UOWDep,
                       personal_number:str):
    
    verify_code = await StudentService().make_verify_code(uow, personal_number=personal_number)
    return {"status":"Ok", "verify_code":verify_code}


@router.get("/verifying_codes",
            status_code=status.HTTP_200_OK,)
async def verify_code(uow: UOWDep,
                       personal_number:str,
                       verification_code:str):
    
    api_token = await StudentService().verify_code(uow, personal_number=personal_number, verification_code=verification_code)
    return api_token