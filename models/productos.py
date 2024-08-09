from sqlalchemy import Column,Integer,String,Float
from Config.database import Base

class producto(Base):
    tablename = 'productos'

    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    precio = Column(Integer)
    cantidad = Column(Integer)