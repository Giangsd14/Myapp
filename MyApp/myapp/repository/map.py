from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas
from ..models import User, Map
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..hashing import Check
from datetime import datetime, timezone
from ..routers import upload_image
from typing import Optional


db_depend = AsyncSession


async def create_map(
    db: db_depend,
    name: str,
    desc: Optional[str],
    category: Optional[str],
    share: bool,
    img: Optional[UploadFile],
    get_current_user
):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    image_url = None
    if img:
        image_url = await upload_image.upload_image(get_current_user, img)
        image_url = image_url.get("url")

    map_instance = Map(
        name=name,
        desc=desc,
        category=category,
        share=share,
        img=image_url,
        author=user.user_name,
        author_id=user.id,
        owner=user.user_name
    )

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

    if map_instance.share:
        from .template import create_template
        return await create_template(db, map_instance.id, get_current_user)
    
    return map_instance
    

async def get_all_map(db: db_depend, get_current_user):
    return await db.scalars(select(Map).where(Map.author == get_current_user.username))


async def get_map(db: db_depend, map_id: int, get_current_user):
    map = await db.scalar(select(Map).where((Map.id == map_id) & (Map.author == get_current_user.username)))
    if not map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map!")
    return map
    

async def delete_map(db: db_depend, map_id: int, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")
    map = await db.scalar(select(Map).where(Map.id == map_id))
    if map.img:
        await upload_image.delete_image(get_current_user, map.img)
    
    await db.delete(map)
    await db.commit()
    return {"detail": "Map deleted!"}


async def update_map(db: db_depend, map_id: int, data: schemas.UpdateMap, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")
    
    map = await db.scalar(select(Map).options(selectinload(Map.templates)).where(Map.id == map_id))
    map_old = map.share
    map.upd_at = datetime.now(timezone.utc)

    update_fields = data.model_dump(exclude_unset=True)
    map_new = update_fields.get("share")
    for key, value in update_fields.items():
        setattr(map, key, value)

    await db.commit()
    await db.refresh(map)

    if map_old == map_new:
        return map
    else:
        if map_new == True:
            from .template import create_template
            return await create_template(db, map.id, get_current_user)
        else:
            from .template import delete_template
            delete_template = await delete_template(db, map.templates[0].id, get_current_user)
            if not delete_template:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your template invalid!")
            raise HTTPException(status_code=200, detail="Template deleted!")