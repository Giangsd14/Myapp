from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.orm import Session
from ..repository import map


router = APIRouter(
    prefix="/map",
    tags=['Map']
)


db_depend = Annotated[Session, Depends(database.get_db)]


@router.post("/", response_model=schemas.CreateMap)
def create_map(db: db_depend, data: schemas.CreateMap, get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return map.create_map(db, data)

@router.get("/", response_model=list[schemas.ShowMap])
def get_all_map(db: db_depend):
    return map.get_all_map(db)

@router.get("/{id}", response_model=schemas.ShowMap)
def get_map(db: db_depend, id: int):
    return map.get_map(db, id)