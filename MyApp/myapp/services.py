from .models import User, Map, user_map
from sqlalchemy.orm import Session
from .schemas import CreateUser, CreateMap
from .hashing import Hash


def create_user(db: Session, data: CreateUser):
    user_instance = User(**data.model_dump())
    user_instance.user_pass = Hash.bcrypt(user_instance.user_pass)
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance

def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def gets_user(db: Session):
    return db.query(User).all()


def create_map(db: Session, data: CreateMap):
    map_instance = Map(**data.model_dump()) #object -> dict -> key_value
    db.add(map_instance)
    db.commit()
    db.refresh(map_instance)

    map_ = db.query(Map).filter_by(id=map_instance.id).first()
    user = db.query(User).filter(User.id == map_instance.author_id).first()
    user.maps.append(map_)
    db.commit()   
    return map_instance

def get_map(db: Session, id: int):
    return db.query(Map).filter(Map.id == id).first()

def gets_map(db: Session):
    return db.query(Map).all()

