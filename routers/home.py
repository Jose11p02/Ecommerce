from fastapi import APIRouter,Depends,Request,Query,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse,HTMLResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
from schemas.productos import producto
from typing import List
from Config.database import localSession
from services.home import HomeServices
from middleware.jwt_bearer import jwtbearer
from sqlalchemy.exc import SQLAlchemyError

Home_router = APIRouter()

templates = Jinja2Templates(directory='templates')

@Home_router.get('/presupuesto/lista',tags=['home'],response_class=HTMLResponse)

def get_lista(request:Request):
    db = localSession()
    try:
        result = HomeServices(db).get_list()
        if not result:
            return templates.TemplateResponse(
                'no_result.html',
                {'request':request, "message":"sin resultados disponibles"},
                status_code=404
            )
        return templates.TemplateResponse(
            'product_list.html',
            {'request':request, 'products':jsonable_encoder(result)},
            status_code=200
        )
    except SQLAlchemyError as e:
         db.rollback()
         return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
         )
    except Exception as e:
            return templates.TemplateResponse(
                'error.html',
                {'request':request,'error': str(e)},
                status_code=500
            )
    finally:
        db.close()

@Home_router.get('/presupuesto/category',tags=['home'],response_class=HTMLResponse)
def get_category(request:Request):
    db = localSession()
    try:
        result = HomeServices(db).get_category()
        if not result:
            return templates.TemplateResponse(
                'no_result.html',
                {'request':request, "message":"sin resultados disponibles"},
                status_code=404
            )
        return templates.TemplateResponse(
            "categories.html", 
            {"request": request, "categories": result},
            status_code=200
        )
    except SQLAlchemyError as e:
         db.rollback()
         return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
         )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
    finally:
         db.close()

@Home_router.get('/presupuesto/for_category',tags=['home'],response_class=HTMLResponse)
def get_for_category(
    request:Request,
    category: str = None
):
    db = localSession()
    try:
        if not category:
            return templates.TemplateResponse(
                'products_for_category.html',
                {'request':request,'products':[],'category':''},
                status_code=400
            )
        result = HomeServices(db).get_product_for_categoria(category)
        if not result:
            return templates.TemplateResponse(
                'no_result.html',
                {'request':request, "message":"sin resultados disponibles"},
                status_code=404
            )
        return templates.TemplateResponse(
            'products_for_category.html',
            {'request':request,'products':result,'category':category},
            status_code=200
        )
    except SQLAlchemyError as e:
         db.rollback()
         return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
         )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
    finally:
         db.close()

@Home_router.get('/presupuesto/add',tags=['home'],response_class=HTMLResponse)
#,dependencies=[Depends(jwtbearer())]
def show_form(request:Request):
        return templates.TemplateResponse(
            'add_product.html',
            {'request':request,'message':None,'error':None}
        )

@Home_router.post('/presupuesto/add',tags=['home'],response_class=HTMLResponse)

def add_product(
     request:Request,
     nombre: str = Form(None),
     precio: float = Form(None),
     categoria: str = Form(None)
):
    db = localSession()
    message = None
    error = None
 
    try:
        if not nombre or not precio or not categoria:
            error = 'Por favor, completa todos los campos.'
        else:
            new_product = producto(nombre=nombre,precio=precio,categoria=categoria)
            HomeServices(db).add_product(new_product)
            message = 'Producto agregado exitosamente. Serás redirigido en unos segundos...'
        return templates.TemplateResponse(
            'add_product.html',
            {'request':request,'message':message,'error':error}
        )
    except SQLAlchemyError as e:
        db.rollback()
        return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
    finally:
        db.close()

@Home_router.get('/presupuesto/buscar',tags=['home'],response_class=HTMLResponse)

async def buscar(request:Request,nombre:str = None):
    db = localSession()
    try:
        busqueda = False
        if nombre:
            busqueda = True
        result = HomeServices(db).get_list_for_name(nombre)
        print(result)
        return templates.TemplateResponse(
            'buscar_producto.html',
            {'request':request,'producto':result,'nombre':nombre,'busqueda':busqueda}
        )
    except SQLAlchemyError as e:
        db.rollback()
        return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
    finally:
        db.close()

@Home_router.get('/presupuesto/buscar_para_actualizar',tags=['home'],response_class=HTMLResponse)
def buscar_para_actualizar(request:Request,nombre:str = None):
    db = localSession()
    try:
        result = HomeServices(db).get_list_for_name(nombre)
        if not result:
            return templates.TemplateResponse(
                'buscar_producto.html',
                {'request':request,'product':result,'nombre':nombre}
            )
        return templates.TemplateResponse(
            'update_product.html',
            {'request':request,'product':result}
        )
    except SQLAlchemyError as e:
        db.rollback()
        return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
    finally:
        db.close()

@Home_router.post('/presupuesto/update',tags=['home'],response_class=HTMLResponse)

def update(
    request:Request,
    nombre: str = Form(None),
    nuevo_nombre:str = Form(None),
    precio: float = Form(None),
    categoria: str = Form(None)
):
    db = localSession()
    try:
        new_product = producto(nombre=nuevo_nombre,precio=precio,categoria=categoria)
        result = HomeServices(db).update_product(nombre,new_product)
        if not result:
            templates.TemplateResponse(
                'error.html',
                {'request':request,'error':'No se pudo actualizar el producto.'},
                status_code=404
            )
        return RedirectResponse(url=f"/presupuesto/buscar?nombre={nuevo_nombre}",status_code=303)
    except SQLAlchemyError as e:
        db.rollback()
        return templates.TemplateResponse(
            'error.html',
            {'request':request, 'error':'error en la base de datos:' + str(e)}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=500
        )
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