from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from .database import Base
from sqlalchemy.orm import relationship



class BaseModel(Base):
    __abstract__ = True #no create table
    __allow_unmapped__ = True #no use mapped

    id = Column(Integer, primary_key=True, index=True)


user_map = Table(
    "user_map",
    Base.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("map_id", ForeignKey("Map.id"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'User'

    user_name = Column(String, index=True)
    user_pass = Column(String, index=True)
    email = Column(String, index=True)
    cre_at = Column(String)

    maps = relationship("Map", secondary=user_map, back_populates="users")


class Map(BaseModel):
    __tablename__ = 'Map'

    author = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("User.id"), index=True)
    name = Column(String, index=True)
    desc = Column(String, index=True)
    img = Column(String, index=True)
    cre_at = Column(String)
    upd_at = Column(String)
    share = Column(Boolean)

    users = relationship("User", secondary=user_map, back_populates="maps")
    templates = relationship("Template", back_populates="maps", uselist=False, cascade="all, delete-orphan")
    points = relationship("Point", back_populates="maps", uselist=False, cascade="all, delete-orphan")


class Template(BaseModel):
    __tablename__ = 'Template'

    map_id = Column(Integer, ForeignKey("Map.id"), primary_key=True)
    no_like = Column(Integer, index=True)

    maps = relationship("Map", back_populates="templates")


class Point(BaseModel):
    __tablename__ = 'Point'

    name = Column(String, index=True)
    geom = Column(String, index=True)
    desc = Column(String, index=True)
    img = Column(String, index=True)
    cre_at = Column(String)
    upd_at = Column(String)
    map_id = Column(Integer, ForeignKey("Map.id"))

    maps = relationship("Map", back_populates="points")


