from fastapi import (
    status, 
    HTTPException, 
    Depends,
    APIRouter
)

from apps.utils import get_hash_password
from dotenv import load_dotenv
load_dotenv()


from apps.schema import (
    AuthUsers,
    UserResponse
)

from .. import models
from sqlalchemy.orm  import Session
from ..database import (
    get_db
)

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, 
          response_model=UserResponse)
def create_user(user:AuthUsers, db:Session = Depends(get_db)):
    
    # hash the pswd - user.password
    hashed_pswd = get_hash_password(user)
    user.password = hashed_pswd
    # convert the user to dict and unpack it to the authUser  b2aise4
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    
    return new_user
    
@router.get('/{id}', response_model=UserResponse)  
# Retrieve user
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with id: {id} does not exist')

    return user


