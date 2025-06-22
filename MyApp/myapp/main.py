from .routers import login, user, map, point, template, feedback, upload_image
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import cloudinary
from cloudinary.uploader import upload
from PIL import Image
import io
from .config import settings 


app = FastAPI(docs_url="/")


app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,  # or ["*"] for test
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login.router)
app.include_router(map.router)
app.include_router(user.router)
app.include_router(point.router)
app.include_router(template.router)
app.include_router(feedback.router)
app.include_router(upload_image.router)
