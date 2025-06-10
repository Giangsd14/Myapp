from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, token
from ..hashing import Hash
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=['Login'])

db_depend = Annotated[Session, Depends(database.get_db)]
mydata = Annotated[OAuth2PasswordRequestForm, Depends()]
@router.post("/login")
def login(db: db_depend, data: mydata) -> schemas.Token:
    user = db.query(models.User).filter(models.User.user_name == data.username).first()
    print(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username!")
    if not Hash.verify(data.password, user.user_pass): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password!")
    
    access_token = token.create_access_token(data={"sub": user.user_name})
    return schemas.Token(access_token=access_token, token_type="bearer")
