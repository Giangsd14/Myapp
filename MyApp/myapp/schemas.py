from datetime import date
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
    cre_at: date

class MapBase(BaseModel):
    name: str
    author: str
    author_id: int
    desc: str
    img: str
    cre_at: date 
    upd_at: date 
    share: bool = False


class CreateUser(UserBase):
    pass

class CreateMap(MapBase):
    pass


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
    cre_at: date

    class config:
        from_attribute = True

class ShowMap(BaseModel):
    id: int
    name: str
    users: list[ShowUser]

    class config:
        orm_mode = True


class Template(BaseModel):
    no_like: int = 0

class Like_Map(BaseModel):
    id_user: int | None = None
    map_id: int | None = None