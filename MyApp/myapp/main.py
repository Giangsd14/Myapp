from fastapi import FastAPI
from .database import engine, Base
from .routers import login, user, map

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(map.router)
app.include_router(user.router)
