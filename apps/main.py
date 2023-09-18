from fastapi import (
    FastAPI, 
    Depends
)

import os 
import time
from dotenv import load_dotenv
load_dotenv()

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
from apps.routers import posts, users, auth

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


app.include_router(posts.router, prefix='/posts', tags=['Posts'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(auth.router, tags=['Authentication'])