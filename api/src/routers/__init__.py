from api.src.routers.students import router as student_router
from api.src.routers.finance import router as finance_router


all_routers = [
    student_router,
    finance_router,
]