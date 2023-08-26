from fastapi import (
    FastAPI, 
    Response, 
    status, 
    HTTPException, 
    Depends
)
import os 
import time
from dotenv import load_dotenv
load_dotenv()


from pydantic import BaseModel
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
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



app = FastAPI()


""" 
Your api has to be validated and constraints to avoid the clients 
sending any gibberish
"""
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True,
    
    
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

@app.get('/posts')
def test_post(db:Session = Depends(get_db)):
    return {'status': 'success '}

@app.get('/login')
async def student_info():
    generate_password = create_ref_code()
    return {
        'message': generate_password 
     }


# request comes in with path '/' and first one wins based in order
@app.get('/posts')
def get_post():
    cursor.execute(""" SELECT * FROM post """)
    posts = cursor.fetchall()
    print(posts)
    return {'data':posts}


#post request
@app.post("/posts", status_code=status.HTTP_201_CREATED) # status code changed
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO post(title, content, published)
            VALUES (%s, %s, %s) RETURNING * """,
            (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post }

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
@app.get("/posts/{id}") # the id field represent the patch param
def get_post(id: int): # convert it here 
    
    #convert the int to string before passing
   cursor.execute(""" SELECT * FROM Post where id = %s returning * """, str((id),))
   new_post = cursor.fetchone()
   print(new_post)
   post = find_post(id)
   if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} was not found")
   return {"post_detail": post}



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post 4:25hr
    # find th index in the array that has required ID
    # my_posts.pop(id)
    
    cursor.execute(""" DELETE  FROM post WHERE id = %s RETURNING * """, str((id),))
    delete_post = cursor.fetchone() 
    conn.commit()
    if delete_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
 
    # deleting something has to be retrieved via 204 -> you must do it
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
# we adhere to schema models to avoid clients sending anything they want.
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
  
    return {"message": updated_post}

#hr mins





