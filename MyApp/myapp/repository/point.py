from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from .. import schemas

from ..models import User, Map, Point
from ..hashing import Check
from sqlalchemy import select



db_depend = AsyncSession

async def create_point(db: db_depend, data: schemas.CreatePoint, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    point_instance = Point(**data.model_dump())
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == point_instance.map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")

    db.add(point_instance)
    await db.commit()
    await db.refresh(point_instance) 

    return point_instance


async def get_all_point(db: db_depend, map_id: int):
    return await db.scalars(select(Point).where(Point.map_id == map_id))

async def get_point(db: db_depend, map_id: int, point_id: int):
    return await db.scalar(select(Point).where((Point.map_id == map_id) & (Point.id == point_id)))

async def delete_point(db: db_depend, map_id: int, point_id: int, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")

    point = await db.scalar(select(Point).where((Point.map_id == map_id) & (Point.id == point_id)))

    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Point!")
    
    await db.delete(point)
    await db.commit()
    return {"detail": "Point deleted!"}

async def update_point(db: db_depend, map_id: int, point_id: int, data: schemas.UpdatePoint, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")

    point = await db.scalar(select(Point).where((Point.map_id == map_id) & (Point.id == point_id)))
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Point!")
    
    point.upd_at = datetime.now(timezone.utc).replace(tzinfo=None) #.replace(tzinfo=None)  tạm

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(point, key, value)
        
    await db.commit()
    await db.refresh(point)
    return point