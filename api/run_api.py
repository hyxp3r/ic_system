from fastapi import FastAPI

from api.src.routers import all_routers

app = FastAPI(title='ic_system', root_path='/api/v1')


for router in all_routers:
    app.include_router(router)
