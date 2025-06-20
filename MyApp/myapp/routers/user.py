from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import user


router = APIRouter(
    prefix="/user",
    tags=['User']
)

db_depend = Annotated[AsyncSession, Depends(database.get_db)]

@router.post("/", response_model=schemas.User)
async def new_user(db: db_depend, data: schemas.CreateUser):
    return await user.new_user(db, data)

@router.get("/", response_model=list[schemas.ShowUser])
async def get_all_user(db: db_depend, get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await user.get_all_user(db)

@router.get("/{id}", response_model=schemas.User)
async def get_user(db: db_depend, id: int):
    return await user.get_user(db, id)