from fastapi import FastAPI
from .routers import login, user, map


app = FastAPI(docs_url="/")


app.include_router(login.router)
app.include_router(map.router)
app.include_router(user.router)
