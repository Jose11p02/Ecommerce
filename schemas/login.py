from pydantic import BaseModel,Field
from typing import Optional

class login(BaseModel):
    id:Optional[int] = None
    usuario:str
    contraseña:str

    class Config:
        json_schema_extra = {
            'example':{
                'usuario': 'jose@gmail.com',
                'contraseña': 'jaja123'
            }
        }