from models.car import Car
from schemas.car import car

class CarServices():
    def __init__(self,db) -> None:
        self.db = db

    def get_car(self,user_id):
        result = self.db.query(Car).filter(Car.user_id == user_id).all()
        return result
    
    def add(self,car:car,user_id:int):
        new_item = Car(**car.model_dump(),user_id = user_id)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)

    def vaciar(self,user_id):
        self.db.query(Car).filter(Car.user_id == user_id).delete()
        self.db.commit()

    def delete(self,id,user_id):
        result = self.db.query(Car).filter(Car.user_id == user_id,Car.id == id).first()
        self.db.delete(result)
        self.db.commit()

    def total(self,user_id):
        item = self.db.query(Car).filter(Car.user_id == user_id).all()
        total = 0
        for i in item:
            total +=  i.producto.precio * i.cantidad
            print(total)
        result = total
        return result

    def mas(self,id,user_id):
        result = self.db.query(Car).filter(Car.user_id == user_id,Car.id == id).first()
        if result:
            result.cantidad = result.cantidad + 1
            self.db.commit()

    def menos(self,id,user_id):
        result = self.db.query(Car).filter(Car.user_id == user_id,Car.id == id).first()
        if result:
            if result.cantidad >= 1:
                result.cantidad = result.cantidad - 1
            if result.cantidad == 0:
                self.db.delete(result)
            self.db.commit()