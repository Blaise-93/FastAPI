from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

""" 
Your api has to be validated and constraints to avoid the clients 
sending any gibberish
"""
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True

@app.get("/")
async def root():
    return {'message': 'Hello Blaise'}

@app.get('/login')
async def student_info():
    new_student_position = []
    new_position = [90, 42, 40, 67, 89, 50, 100]
    for position in new_position:
        if position % 2 == 0:
            new_student_position.append(position)
            print(new_student_position)
            return {
                'message': 'Hello Blaise',
                'age': 25,
                'student_positions': new_student_position
                }


# request comes in with path '/' and first one wins based in order
@app.get('/post')
def get_post():
    return {'data': "Blaise will you be available tonight?"}


#post request
@app.post("/create-posts")

def create_posts(new_post: Post):
    figure = 30
    print(new_post)

    return {"data": "new post"}

#1hr 18mins





