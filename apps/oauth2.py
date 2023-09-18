import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from  .schema import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

 
load_dotenv()

# secretkey
# algo
#expiration time

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    
     try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        id:str = payload.get('user_id')
        
        if id is None:
            raise credentials_exception
        # we can pass more data in tokendata
        token_data = TokenData(id=id)
        return token_data
         
     except JWTError:
         raise credentials_exception
         
         
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials ",
        headers={"WWW-Authenticate":"Bearer" })
    
    return verify_access_token(token, credentials_exception )