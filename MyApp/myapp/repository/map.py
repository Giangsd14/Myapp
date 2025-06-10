from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from .. import schemas, database, services

db_depend = Annotated[Session, Depends(database.get_db)]

def create_map(db: db_depend, data: schemas.CreateMap):
    return services.create_map(db, data)

def get_all_map(db: db_depend):
    return services.gets_map(db)

def get_map(db: db_depend, id: int):
    map_query_set = services.get_map(db, id)
    if not map_query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid map hihi!")
    return map_query_set