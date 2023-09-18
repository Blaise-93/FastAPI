
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def get_hash_password(user):
      # hash the pswd - user.password
    hashed_pswd = pwd_context.hash(user.password)
    return hashed_pswd
  

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
  