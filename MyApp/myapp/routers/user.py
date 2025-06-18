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
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/", response_model=schemas.User)
async def new_user(db: db_depend, data: schemas.CreateUser):
    return await user.create_user(db, data)

@router.get("/", response_model=list[schemas.ShowUser])
async def get_all_user(db: db_depend, get_current_user: current_user):
    return await user.get_all_user(db)

@router.get("/{id}", response_model=schemas.User)
async def get_user(db: db_depend, id: int):
    return await user.get_user(db, id)

@router.delete("/")
async def delete_account(db: db_depend, password: str, get_current_user: current_user):
    return await user.delete_account(db, password, get_current_user)

@router.put("/", response_model=schemas.MessageResponse)
async def update_password(db: db_depend, password: str, get_current_user: current_user, data: schemas.CreateUser):
    return await user.update_password(db, password, get_current_user, data)

@router.post("/like", response_model=schemas.Like_Map)
async def like_map(db: db_depend, temp_id: int, get_current_user: current_user):
    return await user.like_map(db, temp_id, get_current_user)