#python init_db.py
import asyncio
from myapp.database import Base, engine
from myapp import models

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())
