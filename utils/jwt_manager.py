from fastapi import Depends,HTTPException,status
from jose import JWTError
from jose.jwt import decode
from Config.database import SECRETE_KEY
from middleware.jwt_bearer import jwtbearer 

def get_current_user(token:str = Depends(jwtbearer())):
    try:
        payload = decode(token,key=SECRETE_KEY,algorithms=['HS256'])
        user_id: int = payload.get('user_id')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o sin user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )