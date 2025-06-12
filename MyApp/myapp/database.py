from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session
