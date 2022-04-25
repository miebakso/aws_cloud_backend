from typing import Optional
from datetime import datetime

from pydantic import BaseModel

SUCCESS = {
    'Detail': 'success'
}

FAIL = {
    'Detail': 'fail'
}

#### Role Models

class RoleCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Role(RoleCreate):
    id: int



#### User Models
class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True

class Login(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    role_id: int
    name: str



#### Post Models

class PostBase(BaseModel):
    title: str
    s3_img: str
    content: str

    class Config:
        orm_mode = True
    
class PostCreate(PostBase):
    post_datetime: datetime
    user_id: int

class PostCreate2(PostBase):
    user_id: int

class PostCreate3(BaseModel):
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True

class PostUpdate(BaseModel):
    title: str
    s3_img: Optional[str]
    content: str

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    post_datetime: datetime
    user_id: int
    is_active: bool
    n_like: int

class PostDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True

class PostComment(Post):
    comments: list = []

    


#### Comment Models

class CommentBase(BaseModel):
    message: str
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class CommentCreate(CommentBase):
    msg_datetime: datetime

class Comment(BaseModel):
    id: int
    message: str
    msg_datetime: datetime
    user_id: int
    username: str
    
    class Config:
        orm_mode = True
    



#### Likes Models

class LikeBase(BaseModel):
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
