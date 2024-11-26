from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class login(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    usuario = Column(String)
    contraseña = Column(String)

    Car = relationship('Car',back_populates='login')