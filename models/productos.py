from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship
from Config.database import Base

class producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    precio = Column(Integer)
    categoria =Column(String)

    Car = relationship('Car',uselist=False,back_populates='producto',single_parent=True)