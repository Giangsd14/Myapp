from __future__ import annotations
from unicodedata import category
from sqlalchemy import Column, ForeignKey, String, Table, DateTime
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone



class BaseModel(Base):
    __abstract__ = True #no create table

    id: Mapped[int] = mapped_column(primary_key=True)


user_map = Table(
    "user_map",
    Base.metadata,
    Column("user_id", ForeignKey("User.id", ondelete="CASCADE"), primary_key=True),
    Column("map_id", ForeignKey("Map.id", ondelete="CASCADE"), primary_key=True)
)

user_liked = Table(
    "user_liked",
    Base.metadata,
    Column("user_id", ForeignKey("User.id", ondelete="CASCADE"), primary_key=True),
    Column("temp_id", ForeignKey("Template.id", ondelete="CASCADE"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'User'

    user_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_pass: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] =mapped_column(String, unique=True, index=True)
    cre_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    maps: Mapped[list[Map]] = relationship(secondary=user_map, back_populates="users")
    temps: Mapped[list[Template]] = relationship(secondary=user_liked, back_populates="users")



class Map(BaseModel):
    __tablename__ = 'Map'

    author: Mapped[str] = mapped_column(String, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    desc: Mapped[str] = mapped_column(String)
    img: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    cre_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    upd_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    share: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list[User]] = relationship(secondary=user_map, back_populates="maps", passive_deletes=True)
    templates: Mapped[list[Template]] = relationship(back_populates="maps", cascade="all, delete-orphan")
    points: Mapped[list[Point]] = relationship(back_populates="maps", cascade="all, delete-orphan")


class Template(BaseModel):
    __tablename__ = 'Template'

    map_id: Mapped[int] = mapped_column(ForeignKey("Map.id"))
    no_like: Mapped[int] = mapped_column(default=False)

    maps: Mapped[Map] = relationship(back_populates="templates")
    users: Mapped[list[User]] = relationship(secondary=user_liked, back_populates="temps", passive_deletes=True)


class Point(BaseModel):
    __tablename__ = 'Point'

    name: Mapped[str] = mapped_column(String, index=True)
    geom: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    img: Mapped[str] = mapped_column(String)
    cre_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    upd_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    map_id: Mapped[int] = mapped_column(ForeignKey("Map.id"))

    maps: Mapped[list[Map]] = relationship(back_populates="points")
    
