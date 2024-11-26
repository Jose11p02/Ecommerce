from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from utils.auth import validate_token
from jose import JWTError

class jwtbearer(HTTPBearer):
    def __init__(self,auto_error: bool = True):
        super(jwtbearer,self).__init__(auto_error=auto_error)
    
    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtbearer,self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,detail='Invalid authentication scheme.')
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail='Invalid token or expired token.')
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403,detail='Invalid authorization code.')
        
    def verify_jwt(self,jwt_token: str):
        try:
            payload = validate_token(jwt_token)
            return True
        except JWTError:
            return False