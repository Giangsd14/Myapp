import email
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, user_liked
from ..hashing import Hash
from .. import database, schemas
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError


db_depend = Annotated[AsyncSession, Depends(database.get_db)]

async def existing_check(db: db_depend, table, whereclause) -> bool:
    existing = await db.scalar(select(table).where(whereclause))
    return existing is not None


async def create_user(db: db_depend, data: schemas.CreateUser):

    if await existing_check(db, User, (User.user_name == data.user_name)):
        # print(await db.scalar(select(User).where(User.user_name == data.user_name)))
        raise HTTPException(400, detail="Username already exists xx")
    if await existing_check(db, User, ((User.email == data.email))):
        raise HTTPException(400, detail="Email already exists")

    user_instance = User(**data.model_dump())
    user_instance.user_pass = Hash.bcrypt(user_instance.user_pass)
    db.add(user_instance)
    try:
        await db.commit()
        await db.refresh(user_instance)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
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


async def update_password(db: db_depend, password: str, get_current_user, data: schemas.CreateUser):
    user_instance = User(**data.model_dump())
    stmt = select(User).where(User.user_name == get_current_user.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    if not Hash.verify(password, user.user_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")
    
    user.user_pass = Hash.bcrypt(user_instance.user_pass)
    await db.commit()
    await db.refresh(user)
    return {
    "detail": "Đổi mật khẩu thành công. Vui lòng đăng nhập lại.",
    "force_logout": True}

async def like_map(db: db_depend, temp_id: int, get_current_user):
    stmt = select(User).where(User.user_name == get_current_user.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    stmt = insert(user_liked).values(user_id=user.id, temp_id=temp_id)
    try:
        result2 = await db.execute(stmt)
        await db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something wrong!")
    return result2
