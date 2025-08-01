from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import map
from fastapi import UploadFile, File, Form


router = APIRouter(
    prefix="/map",
    tags=['Map']
)


db_depend = Annotated[AsyncSession, Depends(database.get_db)]
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/", response_model=schemas.ShowMap)
async def create_map(db: db_depend, data: schemas.CreateMap, get_current_user: current_user):
    return await map.create_map(db, data, get_current_user)

@router.get("/", response_model=list[schemas.ShowMap])
async def get_all_map(db: db_depend, get_current_user: current_user):
    return await map.get_all_map(db, get_current_user)

@router.get("/{map_id}", response_model=schemas.ShowMap)
async def get_map(db: db_depend, map_id: int, get_current_user: current_user):
    return await map.get_map(db, map_id, get_current_user)

@router.delete("/")
async def delete_map(db: db_depend, map_id: int, get_current_user: current_user):
    return await map.delete_map(db, map_id, get_current_user)

@router.put("/", response_model=schemas.ShowMap | schemas.ShowTemplate)
async def update_map(db: db_depend, map_id: int, data: schemas.UpdateMap, get_current_user: current_user):
    return await map.update_map(db, map_id, data, get_current_user)