from fastapi import FastAPI

from api.src.routers import all_routers
from api.tasks import update_finance_table, update_students_table


def create_app():
    update_students_table()
    update_finance_table()
    app = FastAPI(title='ic_system', root_path='/api/v1')
    for router in all_routers:
        app.include_router(router)
    return app


app = create_app()
