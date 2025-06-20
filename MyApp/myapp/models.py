from __future__ import annotations
from sqlalchemy import Column, ForeignKey, String, Table
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime



class BaseModel(Base):
    __abstract__ = True #no create table

    id: Mapped[int] = mapped_column(primary_key=True)


user_map = Table(
    "user_map",
    Base.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("map_id", ForeignKey("Map.id"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'User'

    user_name: Mapped[str] = mapped_column(String, index=True)
    user_pass: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] =mapped_column(String, index=True)
    cre_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    maps: Mapped[list[Map]] = relationship(secondary=user_map, back_populates="users")


class Map(BaseModel):
    __tablename__ = 'Map'

    author: Mapped[str] = mapped_column(String, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("User.id"), index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    desc: Mapped[str] = mapped_column(String)
    img: Mapped[str] = mapped_column(String)
    cre_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    upd_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    share: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list[User]] = relationship(secondary=user_map, back_populates="maps")
    templates: Mapped[list[Template]] = relationship(back_populates="maps", uselist=False, cascade="all, delete-orphan")
    points: Mapped[list[Point]] = relationship(back_populates="maps", uselist=False, cascade="all, delete-orphan")


class Template(BaseModel):
    __tablename__ = 'Template'

    map_id: Mapped[int] = mapped_column(ForeignKey("Map.id"), primary_key=True)
    no_like: Mapped[int] = mapped_column(index=True)

    maps: Mapped[list[Map]] = relationship(back_populates="templates")


class Point(BaseModel):
    __tablename__ = 'Point'

    name: Mapped[str] = mapped_column(String, index=True)
    geom: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    img: Mapped[str] = mapped_column(String)
    cre_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    upd_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    map_id: Mapped[int] = mapped_column(ForeignKey("Map.id"), primary_key=True)

    maps: Mapped[list[Map]] = relationship(back_populates="points")


