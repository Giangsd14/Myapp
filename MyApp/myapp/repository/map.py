from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database

from ..models import User, Map
from ..hashing import Hash, Check
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload


db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def create_map(db: db_depend, data: schemas.CreateMap, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    map_instance = Map(**data.model_dump()) #object -> dict -> key_value
    map_instance.author = user.user_name
    map_instance.author_id = user.id
    
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

async def get_map(db: db_depend, map_id: int):
    map = await db.scalar(select(Map).where(Map.id == map_id))
    if not map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map!")
    return map
    
async def delete_map(db: db_depend, map_id: int):
    map = await db.scalar(select(Map).where(Map.id == map_id))
    
    if not map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map!")
   
    await db.delete(map)
    await db.commit()
    return {"detail": "Map đã được xóa"}
