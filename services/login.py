from schemas.login import login
from models.users import login as M_login
from utils.auth import create_token

class loginServices():
    def __init__(self,db):
        self.db = db

    def register(self,login:login):
        new_user = M_login(**login.model_dump())
        self.db.add(new_user)
        self.db.commit()

    def acceder(self,login:login):
        result = self.db.query(M_login).filter(M_login.usuario == login.usuario,M_login.contraseña == login.contraseña).first()
        user_data = {'sub':result.usuario,'user_id':result.id}
        token = create_token(user_data)
        return token