from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from schemas.producto import producto
from typing import List

app = FastAPI()

app.title = 'tienda online'

app.version = '1.1'

lista = [{
    'id':1,
    'nombre':'leche',
    'precio':1.80,
    'cantidad':2}
    ]

@app.get('/presupuesto/message',tags=['home'])

def hola():
    return HTMLResponse('<h1>hola</h1>')

@app.get('/presupuesto/lista',tags=['lista'],response_model=List[producto])

def get_lista():
    return JSONResponse(status_code=200,content=lista)

@app.get('/presupuesto/{id}',tags=['lista'])

def for_id(id:int):
    return [item for item in lista if item['id'] == id]

@app.post('/presupuesto/add',tags=['lista'],response_model=List[producto])

def add(producto:producto)-> producto:
    lista.append(producto.model_dump())
    return JSONResponse(status_code=202,content={'message':'add'})

@app.put('/presupuesto/update/{id}',tags=['lista'])

def update(id:int,Producto:producto):
    for i in lista:
        if i["id"] == id:
            i['nombre'] = Producto.nombre
            i['precio'] = Producto.precio
            i['cantidad'] = Producto.cantidad
    
    return JSONResponse(status_code=200,content={'message':'update'})

@app.delete('/presupuesto/{id}',tags=['lista'],response_model=List[producto])

def delete(id:int):
    for p in lista:
        if p['id'] == id:
            lista.remove(p)
    return JSONResponse(status_code=200,content={'message':'delete'})