from .models import User, Map
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateUser, CreateMap
from .hashing import Hash
from sqlalchemy import select
from sqlalchemy.orm import selectinload



async def create_user(db: AsyncSession, data: CreateUser):
    user_instance = User(**data.model_dump())
    user_instance.user_pass = Hash.bcrypt(user_instance.user_pass)
    db.add(user_instance)
    await db.commit()
    await db.refresh(user_instance)
    return user_instance

async def get_user(db: AsyncSession, id: int):
    stmt = select(User).where(User.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def gets_user(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_map(db: AsyncSession, data: CreateMap):
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

async def get_map(db: AsyncSession, id: int):
    stmt = select(Map).options(selectinload(Map.users)).where(Map.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def gets_map(db: AsyncSession):
    stmt = select(Map).options(selectinload(Map.users))
    result = await db.execute(stmt)
    return result.scalars().all()

