from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.car import car
from typing import List
from Config.database import localSession
from models.car import Car as carModel
from services.car import CarServices 

car_router = APIRouter()

@car_router.get('/car',tags=['car'])
def get_products():
    db = localSession()
    result = CarServices(db).get_car()
    if not result:
        return JSONResponse(status_code=404,content='car is null') 
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@car_router.post('/car/add',tags=['car'])
def add_item(car:car):
    db = localSession()
    CarServices(db).add(car)
    return JSONResponse(status_code=200, content='add')

@car_router.delete('/car/delete{id}',tags=['car'])
def delete_product(id:int):
    db =localSession()
    CarServices(db).delete(id)
    return JSONResponse(status_code=200,content='delete')

@car_router.get('/car/total',tags=['car'])
def total():
    db = localSession()
    result = CarServices(db).total()
    if not result:
        return JSONResponse(status_code=404,content='car is null') 
    return JSONResponse(status_code=200,content=result)
    
@car_router.put('/car/+',tags=['car'])
def mas(id):
    db = localSession()
    CarServices(db).mas(id)
    return JSONResponse(status_code=200,content='mas')

@car_router.put('/car/-',tags=['car'])
def menos(id):
    db = localSession()
    CarServices(db).menos(id)
    return JSONResponse(status_code=200,content='menos')