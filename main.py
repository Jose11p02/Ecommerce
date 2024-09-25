from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Config.database import Base,engine
from routers.home import Home_router
from routers.car import car_router

app = FastAPI()

app.title = 'tienda online'

app.version = '1.5'

app.include_router(Home_router)

app.include_router(car_router)

Base.metadata.create_all(bind=engine)

