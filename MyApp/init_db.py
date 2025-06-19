#python init_db.py
import asyncio
from myapp.database import Base, engine
from myapp import models
from sqlalchemy import text


async def drop_all_with_cascade():
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))

async def async_main():
    await drop_all_with_cascade()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())