from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import random
import string
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
    published: bool = True
    
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

@app.get('/login')
async def student_info():
    generate_password = create_ref_code()
    return {
        'message': generate_password 
     }


# request comes in with path '/' and first one wins based in order
@app.get('/posts')
def get_post():
    return {'data': my_posts}


#post request
@app.post("/posts", status_code=status.HTTP_201_CREATED) # status code changed
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    print(my_posts) 
    return {"data": post_dict}

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
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} was not found")
    return {"post_detail": post}



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find th index in the array that has required ID
    # my_posts.pop(id)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_posts.pop(index)
    # deleting something has to be retrieved via 204 -> you must do it
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
# we adhere to schema models to avoid clients sending anything they want.
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
  
    """ converts json obj to python dict """
    post_dict = post.dict()
    """ id of the post_dict should be parsed to the list array """
    post_dict['id'] = id
    """ updated post should be set to post_dict coming from front-end """
    my_posts[index] = post_dict
    return {"message": post_dict}

#hr mins




