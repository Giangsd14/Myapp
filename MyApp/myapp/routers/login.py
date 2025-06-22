import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, database, models, token
from ..hashing import Hash
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=['Login'])

db_depend = Annotated[AsyncSession, Depends(database.get_db)]
mydata = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token")
async def login(db: db_depend, data: mydata) -> schemas.Token:
    stmt = select(models.User).where(models.User.user_name == data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    if not Hash().verify(data.password, user.user_pass): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")
    
    access_token = token.create_access_token(data={"sub": user.user_name})
    return schemas.Token(access_token=access_token, token_type="bearer")
