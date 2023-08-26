from pydantic import BaseModel
from datetime import datetime

""" 
Your api has to be validated and constraints to avoid the clients 
sending any gibberish
"""
# Handles and shapi API requests from clients side
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
 
    
class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True
    

class PostCreate(PostBase):
    pass


""" For response valdation cycle of what the frontend
needs. And you can modify it whichever way you want."""
class ResponseUserPost(PostBase):
     id: int
     created_at: datetime
     
     """ stringify the dicts coming from orm -> sqlalchemy
     to real python dicts"""
     class Config:
         orm_mode = True

 

    

    
    
    