from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import StrictInt

class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class UserResponse(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime

    class Config:
        form_attribute = True

class Posts(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner: UserResponse
    
    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    Post: Posts
    count1: int

    class Config:
        from_attributes = True
        # orm_mode = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str

    class Config:
        form_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config: 
        form_attributes = True

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    user_id: int
    post_id: int
    dir: int

    class Config:
        form_attributes= True

class VoteRequest(BaseModel):
    post_id: int
    dir: int

    class Config:
        form_attributes= True
