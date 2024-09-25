from pydantic import BaseModel,Field
from typing import Optional

class car(BaseModel):
    id:Optional[int] = None
    productoId:int
    cantidad:int

    class Config:
        json_schema_extra = {
            'example':{
                'productoId': 2,
                'cantidad': 1
            }
        }