from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.car import car
from typing import List
from Config.database import localSession
from models.car import Car as carModel
from services.car import CarServices 
from middleware.jwt_bearer import jwtbearer
from models.car import Car
from utils.jwt_manager import get_current_user

car_router = APIRouter()

@car_router.get('/car',tags=['car'],dependencies=[Depends(jwtbearer())])
def get_products(current_user = Depends(get_current_user)):
    db = localSession()
    try:
        result = CarServices(db).get_car(current_user)
        
        if not result:
            return JSONResponse(status_code=404, content={'message': 'No se encontraron productos'})

        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.delete('/car/vaciar',tags=['car'],dependencies=[Depends(jwtbearer())])
def vaciar(current_user = Depends(get_current_user)):
    db = localSession()
    try:
        CarServices(db).vaciar(current_user)
        return JSONResponse(status_code=200,content={'message': 'carro vaciado'}) 
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.post('/car/add',tags=['car'],dependencies=[Depends(jwtbearer())])
def add_item(car:car,current_user = Depends(get_current_user)):
    db = localSession()
    try:
        CarServices(db).add(car,current_user)
        return JSONResponse(status_code=200, content='add')
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.delete('/car/delete{id}',tags=['car'],dependencies=[Depends(jwtbearer())])
def delete_product(id:int,current_user = Depends(get_current_user)):
    db =localSession()
    try:
        CarServices(db).delete(id,current_user)
        return JSONResponse(status_code=200,content='delete')
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.get('/car/total',tags=['car'],dependencies=[Depends(jwtbearer())])
def total(current_user = Depends(get_current_user)):
    db = localSession()
    try:
        result = CarServices(db).total(current_user)
        if not result:
            return JSONResponse(status_code=404,content='car is null') 
        return JSONResponse(status_code=200,content=result)
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.put('/car/{id}+',tags=['car'],dependencies=[Depends(jwtbearer())])
def mas(id,current_user = Depends(get_current_user)):
    db = localSession()
    try:
        CarServices(db).mas(id,current_user)
        return JSONResponse(status_code=200,content='mas')
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@car_router.put('/car/{id}-',tags=['car'],dependencies=[Depends(jwtbearer())])
def menos(id,current_user = Depends(get_current_user)):
    db = localSession()
    try:
        result = CarServices(db).menos(id,current_user)
        if result:
            return JSONResponse(status_code=200,content='menos')
        else:
             return JSONResponse(status_code=404,content={'message':'no item'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()