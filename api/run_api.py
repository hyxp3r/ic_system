from fastapi import FastAPI

from api.src.routers import all_routers
from api.tasks import update_finance_table, update_students_table
app = FastAPI(title='ic_system', root_path='/api/v1')


for router in all_routers:
    app.include_router(router)



@app.on_event("startup")
def startup_db_client():
   
    #update_finance_table()
    update_students_table()