from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.productos import producto
from typing import List
from Config.database import localSession
from services.home import HomeServices

Home_router = APIRouter()

@Home_router.get('/presupuesto/lista',tags=['home'],response_model=List[producto])

def get_lista():
    db = localSession()
    result = HomeServices(db).get_list()
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@Home_router.get('/presupuesto/category',tags=['home'])
def get_for_category(category):
    db = localSession()
    result = HomeServices(db).get_product_for_categoria(category)
    if not result:
        return JSONResponse(status_code=404,content={'message':'category not found'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@Home_router.post('/presupuesto/add',tags=['home'],response_model=dict)

def add(producto:producto)-> dict:
    db = localSession()
    HomeServices(db).add_product(producto)
    return JSONResponse(status_code=202,content={'message':'add'})

@Home_router.delete('/presupuesto/{id}',tags=['home'],response_model=List[producto])

def delete(id:int):
    db = localSession()
    result = HomeServices(db).get_list_for_id(id)
    if not result:
        return JSONResponse(status_code=404,content={'message':'sin resultado'})
    HomeServices(db).delete_product(result)
    return JSONResponse(status_code=200,content={'message':'delete'})