from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.login import login
from models.users import login as M_login
from typing import List
from Config.database import localSession
from services.login import loginServices

login_router = APIRouter()

@login_router.post('/login/register',tags=['login'])

def register(login:login):
    db = localSession()
    try:
        loginServices(db).register(login)
        return JSONResponse(status_code=200,content={'message':'registrado'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()

@login_router.post('/login/acceder',tags=['login'])

def acceder(login:login):
    db = localSession()
    try:
        token = loginServices(db).acceder(login)
        if token:
            return JSONResponse(status_code=200,content={'access_token':token,'token_type':'bearer'})
        return JSONResponse(status_code=401,content={'message':'usuario o contraseña no encontrado'})
    except Exception as e:
            db.rollback()
            return JSONResponse(status_code=500, content={'error': str(e)})
    finally:
         db.close()