from models.productos import producto as productoModel
from schemas.productos import producto

class carritoServices():
    def __init__(self,db) -> None:
        self.db = db

    def get_list(self):
        result = self.db.query(productoModel).all
        return result
    
    def get_list_for_id(self,id):
        result = self.db.query(productoModel).filter(productoModel.id == id).first()
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
        product.cantidad = data.cantidad
        self.db.commit()