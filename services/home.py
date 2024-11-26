from models.productos import producto as productoModel
from schemas.productos import producto
from models.car import Car
from schemas.car import car

class HomeServices():
    def __init__(self,db) -> None:
        self.db = db

    def get_list(self):
        result = self.db.query(productoModel).all()
        return result
    
    def get_category(self):
        result = self.db.query(productoModel.categoria).distinct().all()
        return [categoria[0] for categoria in result]
    
    def add(self,car:car):
        new_item = Car(**car.model_dump())
        self.db.add(new_item)
        self.db.commit()

    def get_list_for_id(self,id):
        result = self.db.query(productoModel).filter(productoModel.id == id).first()
        return result
    
    def get_product_for_categoria(self,categoria):
        result = self.db.query(productoModel).filter(productoModel.categoria == categoria).all()
        return result
    
    def add_product(self,Producto:producto):
        new_product = productoModel(**Producto.model_dump())
        self.db.add(new_product)
        self.db.commit()

    def delete_product(self,data):
        self.db.delete(data)
        self.db.commit()

    def update_product(self,id,data):
        product = self.db.query(productoModel).filter(productoModel.id == id).first()
        product.nombre = data.nombre
        product.precio = data.precio
        product.categoria = data.categoria
        self.db.commit()