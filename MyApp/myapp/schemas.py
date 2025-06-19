from datetime import datetime
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class MessageResponse(BaseModel):
    detail: str
    force_logout: bool

class UserBase(BaseModel):
    user_name: str
    user_pass: str
    email: str
    cre_at: datetime 

class MapBase(BaseModel):
    name: str
    author: str
    author_id: int
    desc: str
    img: str
    cre_at: datetime 
    upd_at: datetime 
    share: bool = False


class CreateUser(BaseModel):
    user_name: str
    user_pass: str
    email: str

class CreateMap(BaseModel):
    name: str
    desc: str
    img: str
    category: str

    class config:
        from_attribute = True


class User(UserBase):
    id : int

    class config:
        from_attribute = True

class Map(MapBase):
    id : int

    class config:
        from_attribute = True


class ShowUser(BaseModel):
    id: int
    user_name: str
    email: str
    cre_at: datetime

    class config:
        from_attribute = True

class ShowMap(BaseModel):
    id: int
    name: str
    author: str
    author_id: int
    upd_at: datetime 

    class config:
        orm_mode = True


class Template(BaseModel):
    no_like: int = 0

class Like_Map(BaseModel):
    id_user: int 
    map_id: int 


class CreatePoint(BaseModel):
    map_id: int
    name: str
    geom: str
    desc: str
    img: str


class ShowPoint(CreatePoint):

    id: int
    cre_at: datetime
    upd_at: datetime
