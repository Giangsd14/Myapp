from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database, services

db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def create_map(db: db_depend, data: schemas.CreateMap):
    return await services.create_map(db, data)

async def get_all_map(db: db_depend):
    return await services.gets_map(db)

async def get_map(db: db_depend, id: int):
    map_query_set = await services.get_map(db, id)

    if not map_query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map hihi!")
    return map_query_set