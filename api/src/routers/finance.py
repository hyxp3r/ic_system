from typing import List, Optional

from fastapi import APIRouter, Path, status

from api.src.dependencies.uow import UOWDep
from api.schemas.financeDTO import FinanceSchema
from api.services.finance import FinanceService

router = APIRouter(
    prefix="/finances",
    tags=["Finance"],
)

@router.get("",
            response_model=FinanceSchema,
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "model": FinanceSchema, 
                    "description": "Ok Response",
                                     }                   
                      }
            )
async def get_language(uow: UOWDep,
                       personal_number:str):
    
    finances = await FinanceService().get_finance_by_personal_number(uow, personal_number=personal_number)
    return finances