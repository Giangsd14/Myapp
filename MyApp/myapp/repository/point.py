from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from .. import schemas
from ..models import User, Map, Point
from ..hashing import Check
from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import selectinload
from ..routers import upload_image

db_depend = AsyncSession


async def create_point(db, map_id, data, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    if not await Check().existing_check(
        db, Map, (Map.author_id == user.id) & (Map.id == map_id)
):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your map invalid!"
        )

    point_instance = Point(**data.model_dump())
    point_instance.map_id = map_id

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
    
    await upload_image.delete_image(get_current_user, point.img)

    await db.delete(point)
    await db.commit()
    return {"detail": "Point deleted!"}


async def update_point(db, map_id, point_id, data, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your map invalid!")

    point = await db.scalar(select(Point).where((Point.map_id == map_id) & (Point.id == point_id)))
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Point!")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(point, key, value)

    point.upd_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(point)
    return point