from passlib.context import CryptContext
from sqlalchemy import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(self, password: str):
        return pwd_context.hash(password)
    
    def verify(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
class Check():
    async def existing_check(self, db, table, where_clause) -> bool:
        existing = await db.scalar(select(table).where(where_clause))
        return existing is not None

