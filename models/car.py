from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class Car (Base):
    __tablename__ = 'car'

    id = Column(Integer,primary_key=True)
    productoId = Column(Integer,ForeignKey('productos.id'))
    cantidad = Column(Integer)

    producto = relationship('producto',uselist=False,back_populates='Car',lazy='subquery')