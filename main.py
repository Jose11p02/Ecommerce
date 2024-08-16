from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from Config.database import Base,engine
from routers.carrito import carrito_router

app = FastAPI()

app.title = 'tienda online'

app.version = '1.4'

app.include_router(carrito_router)

Base.metadata.create_all(bind=engine)

@app.get('/presupuesto/message',tags=['home'])

def hola():
    return HTMLResponse('<h1>hola</h1>')

