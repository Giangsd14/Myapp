from fastapi import APIRouter, Depends, UploadFile, File, Form
from .. import schemas, database, oauth2
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import point
from typing import Annotated, Optional

router = APIRouter(
    prefix="/point",
    tags=['Point']
)


db_depend = Annotated[AsyncSession, Depends(database.get_db)]
current_user = Annotated[schemas.User, Depends(oauth2.get_current_user)]


@router.post("/", response_model=schemas.ShowPoint)
async def create_point(
    db: db_depend,
    get_current_user: current_user,
    geom: str = Form(...),
    name: str = Form(...),
    desc: Optional[str] = Form(None),
    map_id: int = Form(...),
    img: Optional[UploadFile] = File(None)
):
    return await point.create_point(
        db, geom, name, desc, map_id, img, get_current_user
    )

@router.get("/", response_model=list[schemas.ShowPoint])
async def get_all_point(db: db_depend, map_id: int):
    return await point.get_all_point(db, map_id)

@router.get("/{point_id}", response_model=schemas.ShowPoint)
async def get_point(db: db_depend, map_id: int, point_id: int):
    return await point.get_point(db, map_id, point_id)

@router.delete("/")
async def delete_point(db: db_depend, map_id: int, point_id: int, get_current_user: current_user):
    return await point.delete_point(db, map_id, point_id, get_current_user)


@router.put("/{map_id}/{point_id}", response_model=schemas.ShowPoint)
async def update_point(
    map_id: int,
    point_id: int,
    db: db_depend,
    get_current_user: current_user,
    geom: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    desc: Optional[str] = Form(None),
    img: Optional[UploadFile] = File(None)
):
    from myapp.schemas import UpdatePoint
    data = UpdatePoint(geom=geom, name=name, desc=desc)
    return await point.update_point(db, map_id, point_id, data, img, get_current_user)