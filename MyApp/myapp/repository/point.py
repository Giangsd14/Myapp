from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database

from ..models import User, Map
from ..hashing import Hash
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload



db_depend = Annotated[AsyncSession, Depends(database.get_db)]


async def create_point(db: db_depend, data: schemas.CreatePoint, get_current_user):
    # return await point.create_point(db, data, get_current_user)
    pass

async def get_all_point(db: db_depend):
    # return await point.get_all_point(db)
    pass

async def get_point(db: db_depend, point_id: int):
    # return await point.get_point(db, point_id)
    pass

async def delete_point(db: db_depend, point_id: int, get_current_user):
    # return await point.delete_point(db, point_id)
    pass