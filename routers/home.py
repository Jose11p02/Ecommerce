from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.productos import producto
from typing import List
from Config.database import localSession
from services.home import HomeServices
from middleware.jwt_bearer import jwtbearer

Home_router = APIRouter()

@Home_router.get('/presupuesto/lista',tags=['home'],response_model=List[producto])

def get_lista():
    db = localSession()
    try:
        result = HomeServices(db).get_list()
        if not result:
            return JSONResponse(status_code=404,content={'message':'sin resultado'})
        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
        db.close()

@Home_router.get('/presupuesto/category',tags=['home'])
def get_category():
    db = localSession()
    try:
        result = HomeServices(db).get_category()
        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()

@Home_router.get('/presupuesto/for_category',tags=['home'])
def get_for_category(category):
    db = localSession()
    try:
        result = HomeServices(db).get_product_for_categoria(category)
        if not result:
            return JSONResponse(status_code=404,content={'message':'category not found'})
        return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()

@Home_router.post('/presupuesto/add',tags=['home'],response_model=dict,dependencies=[Depends(jwtbearer())])

def add(producto:producto)-> dict:
    db = localSession()
    try:
        HomeServices(db).add_product(producto)
        return JSONResponse(status_code=202,content={'message':'add'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()

@Home_router.put('/presupuesto/update',tags=['home'],dependencies=[Depends(jwtbearer())])
def update(id,producto:producto):
    db = localSession()
    try:
        HomeServices(db).update_product(id,producto)
        return JSONResponse(status_code=202,content={'message':'update'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()

@Home_router.delete('/presupuesto/{id}',tags=['home'],response_model=List[producto],dependencies=[Depends(jwtbearer())])

def delete(id:int):
    db = localSession()
    try:
        result = HomeServices(db).get_list_for_id(id)
        if not result:
            return JSONResponse(status_code=404,content={'message':'sin resultado'})
        HomeServices(db).delete_product(result)
        return JSONResponse(status_code=200,content={'message':'delete'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()