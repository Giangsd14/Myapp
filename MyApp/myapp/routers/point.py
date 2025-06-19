from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import point


router = APIRouter(
    prefix="/point",
    tags=['Point']
)


db_depend = Annotated[AsyncSession, Depends(database.get_db)]
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/", response_model=schemas.ShowPoint)
async def create_point(db: db_depend, data: schemas.CreatePoint, get_current_user: current_user):
    return await point.create_point(db, data, get_current_user)

@router.get("/", response_model=list[schemas.ShowPoint])
async def get_all_point(db: db_depend, map_id: int):
    return await point.get_all_point(db, map_id)

@router.get("/{point_id}", response_model=schemas.ShowPoint)
async def get_point(db: db_depend, map_id: int, point_id: int):
    return await point.get_point(db, map_id, point_id)

@router.delete("/")
async def delete_point(db: db_depend, map_id: int, point_id: int, get_current_user: current_user):
    return await point.delete_point(db, map_id, point_id, get_current_user)

@router.put("/", response_model=schemas.ShowPoint)
async def update_point(db: db_depend, map_id: int, point_id: int, data: schemas.UpdatePoint, get_current_user: current_user):
    return await point.update_point(db, map_id, point_id, data, get_current_user)