from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix="/user",
    tags=['User']
)

db_depend = Annotated[Session, Depends(database.get_db)]

@router.post("/", response_model=schemas.User)
def new_user(db: db_depend, data: schemas.CreateUser):
    return user.new_user(db, data)

@router.get("/", response_model=list[schemas.ShowUser])
def get_all_user(db: db_depend, get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_all_user(db)

@router.get("/{id}", response_model=schemas.User)
def get_user(db: db_depend, id: int):
    return user.get_user(db, id)