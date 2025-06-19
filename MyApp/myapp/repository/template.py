from string import Template
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from .map import update_map

from .. import schemas

from ..models import User, Map, Template, user_liked
from ..hashing import Check
from sqlalchemy import insert, select, func, update, delete



db_depend = AsyncSession

async def create_template(db: db_depend, map_id: int, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")
    map = await db.scalar(select(Map).where(Map.id == map_id))
    if map.share:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Template already exists")
    update_data = schemas.UpdateMap(share=True)
    await update_map(db, map.id, update_data, get_current_user)

    temp_instance = Template(map_id=map_id)
    db.add(temp_instance)
    await db.commit()
    await db.refresh(temp_instance)    

    return temp_instance


async def get_all_template(db: db_depend):
    return await db.scalars(select(Template))

async def get_template(db: db_depend, temp_id: int):
    
    temp = await db.scalar(select(Template).where(Template.id == temp_id))   
    if not temp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your template invalid!")
    return temp

async def delete_template(db: db_depend, temp_id: int, get_current_user):

    temp = await db.scalar(select(Template).where(Template.id == temp_id))    
    if not temp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your template invalid!")
    
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == temp.map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your template invalid!")    

    update_data = schemas.UpdateMap(share=False)
    await update_map(db, temp.map_id, update_data, get_current_user)

    await db.delete(temp)
    await db.commit()
    return {"detail": "Template deleted!"}

async def like_template(db: db_depend, temp_id: int, get_current_user):
    temp = await db.scalar(select(Template).where(Template.id == temp_id))
    if not temp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your template invalid!")
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    if await Check().existing_check(db, user_liked,
                                        (user_liked.c.user_id == user.id) & (user_liked.c.temp_id == temp.id)):
        stmt = delete(user_liked).where((user_liked.c.user_id == user.id) & (user_liked.c.temp_id == temp.id))
    else:

        stmt = insert(user_liked).values(user_id=user.id, temp_id=temp.id)

    try:
        await db.execute(stmt)

        count_stmt = select(func.count()).select_from(user_liked).where(user_liked.c.temp_id == temp.id)
        count_result = await db.scalar(count_stmt)

        update_stmt = update(Template).where(Template.id == temp.id).values(no_like=count_result)
        await db.execute(update_stmt)

        await db.commit()
        return temp

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong!")

