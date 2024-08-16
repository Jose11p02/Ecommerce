from pydantic import BaseModel,Field
from typing import Optional

class producto(BaseModel):
    id:Optional[int] = None
    nombre:str
    precio:float
    cantidad:Optional[int] = None

    class Config:
        json_schema_extra = {
            'example':{
                'nombre':'leche',
                'precio':1.80,
                'cantidad':2
            }
        }