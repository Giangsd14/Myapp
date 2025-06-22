from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from .map import update_map
from .. import schemas
from ..models import Feedback, User, Map, Template, user_liked
from ..hashing import Check
from sqlalchemy import insert, select, func, update, delete
from sqlalchemy.orm import selectinload



db_depend = AsyncSession


async def create_feedback(db: db_depend, data: schemas.CreateFeedback, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    feedback_instance = Map(**data.model_dump())
    feedback_instance.author = user.user_name
    feedback_instance.author_id = user.id
    
    db.add(feedback_instance)
    await db.commit()
    await db.refresh(feedback_instance)    
    
    return feedback_instance


async def get_all_feedback(db: db_depend, get_current_user):
    return await db.scalars(select(Feedback))

