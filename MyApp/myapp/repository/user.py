from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, services, database


db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def new_user(db: db_depend, data: schemas.CreateUser):
    return await services.create_user(db, data)

async def get_all_user(db: db_depend):
    return await services.gets_user(db)

async def get_user(db: db_depend, id: int):
    user_query_set = await services.get_user(db, id)

    if not user_query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user hihi!")
    return user_query_set
