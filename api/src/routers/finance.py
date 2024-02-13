from fastapi import APIRouter, Depends, status

from api.src.dependencies.uow import UOWDep
from api.src.dependencies.tokens import get_current_user
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
async def get_finance(uow: UOWDep,
                      user =  Depends(get_current_user),
                       ):
    personal_number = user.personal_number
    finances = await FinanceService().get_finance_by_personal_number(uow, personal_number=personal_number)
    return finances