from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import feedback
from typing import Optional


router = APIRouter(
    prefix="/feedback",
    tags=['Feedback']
)


db_depend = Annotated[AsyncSession, Depends(database.get_db)]
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]

@router.post("/", response_model=schemas.ShowFeedback)
async def create_feedback(db: db_depend, data: schemas.CreateFeedback, get_current_user: current_user):
    return await feedback.create_feedback(db, data, get_current_user)

@router.get("/", response_model=list[schemas.ShowFeedback])
async def get_all_feedback(db: db_depend, get_current_user: current_user):
    return await feedback.get_all_feedback(db, get_current_user)
