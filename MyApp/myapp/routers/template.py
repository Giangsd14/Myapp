from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import template


router = APIRouter(
    prefix="/template",
    tags=['Template']
)


db_depend = Annotated[AsyncSession, Depends(database.get_db)]
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/", response_model=schemas.ShowTemplate)
async def create_template(db: db_depend, map_id: int, get_current_user: current_user):
    return await template.create_template(db, map_id, get_current_user)

@router.get("/", response_model=list[schemas.ShowTemplate])
async def get_all_template(db: db_depend, get_current_user: current_user):
    return await template.get_all_template(db, get_current_user)

@router.get("/{temp_id}", response_model=schemas.ShowTemplate)
async def get_template(db: db_depend, temp_id: int, get_current_user: current_user):
    return await template.get_template(db, temp_id, get_current_user)

@router.delete("/")
async def delete_template(db: db_depend, temp_id: int, get_current_user: current_user):
    return await template.delete_template(db, temp_id, get_current_user)

@router.post("/like", response_model=schemas.ShowTemplate2)
async def like_template(db: db_depend, temp_id: int, get_current_user: current_user):
    return await template.like_template(db, temp_id, get_current_user)