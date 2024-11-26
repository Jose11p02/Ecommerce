from jose.jwt import encode,decode
from datetime import datetime,timedelta,timezone
from Config.database import SECRETE_KEY,TOKEN_SCONDS_EXP

def create_token(data:dict):
    data_token = data.copy()
    data_token['exp'] = datetime.now(tz=timezone.utc) + timedelta(hours=TOKEN_SCONDS_EXP)
    token_jwt = encode(data_token,key=SECRETE_KEY,algorithm="HS256")
    return token_jwt

def validate_token(token):
    data = decode(token,key=SECRETE_KEY,algorithms=['HS256'])
    return data