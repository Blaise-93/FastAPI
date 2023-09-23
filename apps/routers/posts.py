from fastapi import (
    Response, 
    status, 
    HTTPException, 
    Depends,
    APIRouter
)

from typing import List
from dotenv import load_dotenv
load_dotenv()


from apps.schema import (
    PostCreate,
    ResponseUserPost,
)
from .. import models, oauth2
from sqlalchemy.orm  import Session
from apps.database import (
    get_db
)

router = APIRouter(
    
)


# request comes in with path '/' and first one wins based in order
@router.get('/', response_model=List[ResponseUserPost])
def get_post(db:Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


#post request
@router.post("/", 
          status_code=status.HTTP_201_CREATED,
          response_model=ResponseUserPost) # status code changed

def create_posts(post: PostCreate, db: Session = Depends(get_db)
                 ,user_id:int = Depends(oauth2.get_current_user)):

    print(user_id)    
    new_post = models.Post(
            **post.dict()
        )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

""" get latest posts -> be careful in your api route naming
be careful to avoid mismatch of api call whether it is get/post etc

"""


""" getting single post"""
@router.get("/{id}", response_model=ResponseUserPost) # the id field represent the patch param
def get_post(id: int, db:Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)): # convert it here 
   
    post = db.query(models.Post)\
        .filter(models.Post.id == id).first()
        
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} was not found")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db),  
                current_user: int = Depends(oauth2.get_current_user)):
  
    delete_post = db.query(models.Post)\
        .filter(models.Post.id == str(id))

    if delete_post.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    delete_post.delete(synchronize_session=False)
    # deleting something has to be retrieved via 204 -> you must do it
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=ResponseUserPost)
# we adhere to schema models to avoid clients sending anything they want.
def update_post(id: int, updated_post: PostCreate, db:Session=Depends(get_db),  
                current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).\
        filter(models.Post.id == id)
    print(current_user.id)
    post = post_query.first()    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
