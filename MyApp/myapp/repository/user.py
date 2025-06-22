from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..hashing import Hash, Check
from .. import schemas
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError


db_depend = AsyncSession


async def create_user(db: db_depend, data: schemas.CreateUser):
    if await Check().existing_check(db, User, (User.user_name == data.user_name)):
        raise HTTPException(400, detail="Username already exists")
    if await Check().existing_check(db, User, ((User.email == data.email))):
        raise HTTPException(400, detail="Email already exists")

    user_instance = User(**data.model_dump())
    user_instance.user_pass = Hash().bcrypt(user_instance.user_pass)
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
    return await db.scalars(select(User))


async def get_user(db: db_depend, get_current_user):
    return await db.scalar(select(User).where(User.user_name == get_current_user.username))


async def delete_account(db: db_depend, password: str, get_current_user):
    user = await db.scalar(select(User).options(selectinload(User.maps)).where(User.user_name == get_current_user.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    if not Hash().verify(password, user.user_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")

    await db.delete(user)
    await db.commit()
    return {"detail": "Tài khoản đã được xóa",
            "force_logout": True}


async def update_password(db: db_depend, password: str, get_current_user, data: schemas.CreateUser):
    user_instance = User(**data.model_dump())
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    if not Hash().verify(password, user.user_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")
    
    user.user_pass = Hash().bcrypt(user_instance.user_pass)
    await db.commit()
    await db.refresh(user)
    return {
    "detail": "Đổi mật khẩu thành công. Vui lòng đăng nhập lại.",
    "force_logout": True}

