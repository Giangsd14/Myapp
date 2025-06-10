from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str
    user_pass: str
    email: str
    cre_at: int = 2024

class MapBase(BaseModel):
    name: str
    author: str
    author_id: int
    desc: str
    img: str
    cre_at: int = 2024
    upd_at: str | None = None
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
    cre_at: str

    class config:
        from_attribute = True

class ShowMap(BaseModel):
    id: int
    name: str
    users: list[ShowUser]

    class config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Template(BaseModel):
    no_like: int = 0

