from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from . import token, database
from sqlalchemy.ext.asyncio import AsyncSession



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db_depend = Annotated[AsyncSession, Depends(database.get_db)]


async def get_current_user(data: Annotated[str, Depends(oauth2_scheme)],
                           db: db_depend):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        return await token.verify_token(data, credentials_exception, db)