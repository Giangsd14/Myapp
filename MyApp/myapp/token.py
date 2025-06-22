from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas
from .models import User
from .config import settings
from .hashing import Check
from sqlalchemy.ext.asyncio import AsyncSession


# openssl rand -hex 32 #Linux
# SECRET_KEY = secrets.token_urlsafe(32)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str, credentials_exception, db: AsyncSession):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        if not await Check().existing_check(db, User, (User.user_name == username)):
                raise credentials_exception
        token_data = schemas.TokenData(username=username)
        return token_data
    except InvalidTokenError:
        raise credentials_exception