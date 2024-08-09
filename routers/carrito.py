from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.productos import producto
from typing import List
from Config.database import localSession
from services.carrito import carritoServices

carrito_router = APIRouter()

@carrito_router.get('/presupuesto/lista',tags=['lista'],response_model=List[producto])

def get_lista():
    db = localSession()
    result = carritoServices(db).get_list()
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@carrito_router.get('/presupuesto/{id}',tags=['lista'])

def for_id(id:int):
    db = localSession()
    result = carritoServices(db).get_list_for_id(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@carrito_router.post('/presupuesto/add',tags=['lista'],response_model=dict)

def add(producto:producto)-> dict:
    db = localSession()
    carritoServices(db).add_product(producto)
    return JSONResponse(status_code=202,content={'message':'add'})

@carrito_router.put('/presupuesto/update/{id}',tags=['lista'])

def update(id:int):
    db = localSession()
    result = carritoServices(db).get_list_for_id(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    carritoServices(db).update_product(id,result)
    return JSONResponse(status_code=200,content={'message':'update'})

@carrito_router.delete('/presupuesto/{id}',tags=['lista'],response_model=List[producto])

def delete(id:int):
    db = localSession()
    result = carritoServices(db).get_list_for_id(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    carritoServices(db).delete_product(id,result)
    return JSONResponse(status_code=200,content={'message':'delete'})