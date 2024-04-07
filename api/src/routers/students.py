from fastapi import APIRouter, status

from api.schemas.studentDTO import StudentSchema
from api.services.student import StudentService
from api.src.dependencies.uow import UOWDep

router = APIRouter(
    prefix='/students',
    tags=['Students'],
)


@router.get(
    '/creating_codes',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Ok Response',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'No students',
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            'description': 'Student don"t have email',
        },
    },
)
async def create_code(uow: UOWDep, personal_number: str):
    email = await StudentService().make_verify_code(uow, personal_number=personal_number)
    return {'status': 'Ok', 'email': email}


@router.get(
    '/verifying_codes',
    response_model=StudentSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'model': StudentSchema,
            'description': 'Ok Response',
        },
    },
)
async def verify_code(uow: UOWDep, personal_number: str, verification_code: str):
    api_token = await StudentService().verify_code(
        uow, personal_number=personal_number, verification_code=verification_code
    )
    user = await StudentService().get_student_by_personal_number(uow, personal_number)
    return user
