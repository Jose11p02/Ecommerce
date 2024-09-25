from models.car import Car
from schemas.car import car

class CarServices():
    def __init__(self,db) -> None:
        self.db = db

    def get_car(self):
        result = self.db.query(Car).all()
        return result
    
    def add(self,car:car):
        new_item = Car(**car.model_dump())
        self.db.add(new_item)
        self.db.commit()

    def delete(self,id):
        result = self.db.query(Car).filter(Car.id == id).first()
        self.db.delete(result)
        self.db.commit()

    def total(self):
        item = self.db.query(Car).all()
        for i in item:
            total =  i.producto.precio * i.cantidad
            print(total)
        result = total
        return result
    
    def mas(self,id):
        result = self.db.query(Car).filter(Car.id == id).first()
        result.cantidad = result.cantidad + 1
        self.db.commit()

    def menos(self,id):
        result = self.db.query(Car).filter(Car.id == id).first()
        if result.cantidad >= 1:
            result.cantidad = result.cantidad - 1
        if result.cantidad == 0:
            self.db.delete(result)
        self.db.commit()