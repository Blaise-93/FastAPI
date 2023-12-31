from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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


""" For response validation cycle of what the frontend
needs. And you can modify it whichever way you want."""
class ResponseUserPost(PostBase):
     id: int
     created_at: datetime
     user_id: int
     
     """ stringify the dicts coming from orm -> sqlalchemy
     to real python dicts"""
     class Config:
         orm_mode = True

 
class AuthUsers(BaseModel):
     email : EmailStr
     id: int
     password: str

    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type:str
    
    """  class Config:
        orm_mode = True """
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    