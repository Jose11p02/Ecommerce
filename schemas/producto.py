from pydantic import BaseModel,Field
from typing import Optional

class producto(BaseModel):
    id:int
    nombre:str
    precio:float
    cantidad:Optional[int] = None

    class Config:
        json_schema_extra = {
            'example':{
                'id':1,
                'nombre':'leche',
                'precio':1.80,
                'cantidad':2
            }
        }