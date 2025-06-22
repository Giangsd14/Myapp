from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from .map import update_map
from .. import schemas
from ..models import User, Map, Template, user_liked
from ..hashing import Check
from sqlalchemy import insert, select, func, update, delete
from sqlalchemy.orm import selectinload



db_depend = AsyncSession


async def create_template(db: db_depend, map_id: int, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not await Check().existing_check(db, Map, (Map.author_id == user.id) & (Map.id == map_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")
    map = await db.scalar(select(Map).where(Map.id == map_id))
    if not map.share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Your map invalid!")

    temp_instance = Template(map_id=map_id)
    db.add(temp_instance)
    await db.commit()
    await db.refresh(temp_instance)   

    stmt = select(Template).options(selectinload(Template.maps)).where(Template.id == temp_instance.id)
    result = await db.execute(stmt)
    temp_instance_map = result.scalar_one() 

    return temp_instance_map


async def get_all_template(db: db_depend, get_current_user):
    stm = select(Template).options(selectinload(Template.users), selectinload(Template.maps))
    result = await db.execute(stm)
    templates = result.scalars().all()

    templates_with_liked_flag = []
    for temp in templates:
        liked = any(user.user_name == get_current_user.username for user in temp.users)

        temp_data = schemas.ShowTemplate(
            id=temp.id,
            map_id=temp.map_id,
            no_like=temp.no_like,
            maps=schemas.ShowMap.from_orm(temp.maps),  # Nếu 1-1
            liked=liked
        )
        templates_with_liked_flag.append(temp_data)

    return templates_with_liked_flag


async def get_template(db: db_depend, temp_id: int, get_current_user):
    stmt = (
        select(Template)
        .where(Template.id == temp_id)
        .options(
            selectinload(Template.maps),   
            selectinload(Template.users)   
        )
    )
    result = await db.execute(stmt)
    temp = result.scalar_one_or_none()

    if not temp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your template invalid!"
        )

    liked = any(user.user_name == get_current_user.username for user in temp.users)

    temp_data = schemas.ShowTemplate(
        id=temp.id,
        map_id=temp.map_id,
        no_like=temp.no_like,
        liked=liked,
        maps=schemas.ShowMap.from_orm(temp.maps) 
    )

    return temp_data


async def delete_template(db: db_depend, temp_id: int, get_current_user):
    from .map import update_map 
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

