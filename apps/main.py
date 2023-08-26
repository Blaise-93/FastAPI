from fastapi import (
    FastAPI, 
    Response, 
    status, 
    HTTPException, 
    Depends
)
import os 
from typing import Optional, List
import time
from dotenv import load_dotenv
load_dotenv()


from .schema import PostCreate, ResponseUserPost
import random
import string
import psycopg2
from  psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm  import Session
from .database import (
    engine, 
    get_db
)

models.Base.metadata.create_all(bind=engine)

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + \
                                  string.digits, k=20))



app = FastAPI()

    
PASSWORD_KEY = os.getenv('PASSWORD_KEY')
HOST_NAME = os.getenv('HOST_NAME')
USER_NAME = os.getenv('USER_NAME')
DB_NAME = os.getenv('DB_NAME')


while True:
    try:
        conn = psycopg2.connect(
            host=HOST_NAME,
            database=DB_NAME, 
            user=USER_NAME, 
            password=PASSWORD_KEY,
            cursor_factory=RealDictCursor
            )
         
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as e:
        print(e)
        time.sleep(2)
    
# let's save our posts in memory
my_posts = [ 
    {
            "id": 1,
            "title": "Blaise is his name",
            "content": "Publication of facts about Blaise",
            "published":"true",
    },
     {
         "id": 2,
        "title": "Favorite food",
        "content": "I like pizza"

    }
    
]

def find_post(id): # lets find id of each post
    for p in my_posts:
        if p['id'] == id: # id passed into the function
            return p

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == int(id):
            """ return the specific post index lookup """
            return index
            

@app.get("/")
async def root():
    return {'message': 'Hello Blaise'}

@app.get('/sqlalchemy')
def test_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {'status': "successfully"}

@app.get('/login')
async def student_info():
    generate_password = create_ref_code()
    return {
        'message': generate_password 
     }


# request comes in with path '/' and first one wins based in order
@app.get('/posts', response_model=List[ResponseUserPost])
def get_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


#post request
@app.post("/posts", 
          status_code=status.HTTP_201_CREATED,
          response_model=ResponseUserPost) # status code changed
def create_posts(post: PostCreate, db: Session = Depends(get_db)):

    print(post.dict())    
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
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    print(post)
    context = {"data" : post}
    return context


""" getting single post"""
@app.get("/posts/{id}", response_model=ResponseUserPost) # the id field represent the patch param
def get_post(id: int, db:Session = Depends(get_db)): # convert it here 
   
    post = db.query(models.Post)\
        .filter(models.Post.id == id).first()
        
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} was not found")
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db) ):
    
    delete_post = db.query(models.Post)\
        .filter(models.Post.id == str(id))

    if delete_post.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    delete_post.delete(synchronize_session=False)
    # deleting something has to be retrieved via 204 -> you must do it
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}", response_model=ResponseUserPost)
# we adhere to schema models to avoid clients sending anything they want.
def update_post(id: int, updated_post: PostCreate, db:Session=Depends(get_db)):
    
    post_query = db.query(models.Post).\
        filter(models.Post.id == id)
   
    post = post_query.first()    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
