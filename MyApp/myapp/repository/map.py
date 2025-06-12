from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database

from ..models import User, Map
from ..hashing import Hash
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload


db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def create_map(db: db_depend, data: schemas.CreateMap):
    map_instance = Map(**data.model_dump()) #object -> dict -> key_value
    db.add(map_instance)
    await db.commit()
    await db.refresh(map_instance)    

    stmt_user = select(User).options(selectinload(User.maps)).where(User.id == map_instance.author_id)
    result = await db.execute(stmt_user)
    user = result.scalar_one()

    if user:
        user.maps.append(map_instance)
        db.add(user)
        await db.commit()

    return map_instance

async def get_all_map(db: db_depend):
    stmt = select(Map).options(selectinload(Map.users))
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_map(db: db_depend, id: int):
    stmt = select(Map).options(selectinload(Map.users)).where(Map.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
    if not map_query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map hihi!")
    return map_query_set