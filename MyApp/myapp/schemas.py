from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import false


#Login
class Login(BaseModel):
    username: str
    password: str


#Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


#Respone
class MessageResponse(BaseModel):
    detail: str
    force_logout: bool


#User
class UserBase(BaseModel):
    user_name: str
    user_pass: str
    email: str
    cre_at: datetime 

class CreateUser(BaseModel):
    user_name: str
    user_pass: str
    email: str

class User(UserBase):
    id : int

class ShowUser(BaseModel):
    id: int
    user_name: str
    email: str
    cre_at: datetime


#Map
class MapBase(BaseModel):
    name: str
    author: str
    author_id: int
    desc: str
    img: str
    cre_at: datetime 
    upd_at: datetime 
    share: bool = False

class CreateMap(BaseModel):
    name: str
    desc: Optional[str] = None
    img: Optional[str] = None
    category: Optional[str] = None
    share: bool = False

class Map(MapBase):
    id : int

class ShowMap(BaseModel):
    id: int
    name: str
    author: str
    author_id: int
    cre_at: datetime 
    upd_at: datetime 
    share: bool = False
    class Config:
        from_attributes = True

class UpdateMap(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    img: Optional[str] = None
    share: Optional[bool] = None

class Like_Map(BaseModel):
    id_user: int 
    map_id: int 


#Point
class CreatePoint(BaseModel):
    map_id: int
    name: str
    geom: str
    desc: Optional[str] = None
    img: Optional[str] = None

class ShowPoint(CreatePoint):
    id: int
    cre_at: datetime
    upd_at: datetime

class UpdatePoint(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    img: Optional[str] = None


#Template
class CreateTemplate(BaseModel):
    id: int
    map_id: int

class ShowTemplate(CreateTemplate):
    no_like: int 
    liked: bool = False
    maps: ShowMap

    model_config = {
        "from_attributes": True
    }
    
class ShowTemplate2(CreateTemplate):
    no_like: int 
