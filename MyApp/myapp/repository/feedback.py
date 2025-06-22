from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas
from ..models import Feedback, User
from sqlalchemy import select


db_depend = AsyncSession


async def create_feedback(db: db_depend, data: schemas.CreateFeedback, get_current_user):
    user = await db.scalar(select(User).where(User.user_name == get_current_user.username))

    feedback_instance = Feedback(**data.model_dump())
    if feedback_instance.star not in [1, 2, 3, 4, 5]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Star invalid!"
        )
    feedback_instance.username = user.user_name
    feedback_instance.user_id = user.id
    
    db.add(feedback_instance)
    await db.commit()
    await db.refresh(feedback_instance)    
    
    return feedback_instance


async def get_all_feedback(db: db_depend, get_current_user):
    return await db.scalars(select(Feedback))

