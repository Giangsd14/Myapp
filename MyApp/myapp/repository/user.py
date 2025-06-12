from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, Map, user_map
from ..hashing import Hash
from .. import database, schemas
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def create_user(db: db_depend, data: schemas.CreateUser):
    user_instance = User(**data.model_dump())
    user_instance.user_pass = Hash.bcrypt(user_instance.user_pass)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)
    return user_instance

async def get_all_user(db: db_depend):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user(db: db_depend, id: int):
    stmt = select(User).where(User.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
    if not user_query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user hihi!")


async def delete_account(db: db_depend, password: str, get_current_user):
    stmt = select(User).options(selectinload(User.maps)).where(User.user_name == get_current_user.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")

    if not Hash.verify(password, user.user_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")

    await db.delete(user)
    await db.commit()
    return {"detail": "Tài khoản đã bị xóa"}
