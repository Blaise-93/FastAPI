from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from apps.schema import Token
from ..utils import verify
from apps.oauth2 import create_access_token

router = APIRouter()

@router.post('/login', response_model=Token )
def student_login(user_credentials:OAuth2PasswordRequestForm=Depends(),
          db: Session = Depends(database.get_db)):
   user = db.query(models.User).filter(
       models.User.email == user_credentials.username).first()
   
   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail='Invalid Credentials')

   if not verify(user_credentials.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                           detail='Invalid Credentials')
   
   # create a token
   access_token = create_access_token(data= {"user_id": user.id })
   
   # return token

   return { "access_token": access_token, "token_type":"bearer"}

